# @title Document AI LangChain Integration
"""Module contains a PDF parser based on Document AI from Google Cloud.

You need to install two libraries to use this parser:
pip install google-cloud-documentai
pip install google-cloud-documentai-toolbox
"""

# imports for the PDF parser
import logging
import re
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator, List, Optional, Sequence

from langchain_core.document_loaders import BaseBlobParser
from langchain_core.document_loaders.blob_loaders import Blob
from langchain_core.documents import Document
from langchain_core.utils.iter import batch_iterate

from langchain_google_community._utils import get_client_info


# imports for cloud storage
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.gcs_directory import GCSDirectoryLoader
from langchain_community.document_loaders.gcs_file import GCSFileLoader
from langchain_community.utilities.vertexai import get_client_info
import re



# imports for displaying rich results
from IPython.display import display, HTML
import markdown as md


# The PDF Parser

if TYPE_CHECKING:
    from google.api_core.operation import Operation  # type: ignore[import]
    from google.cloud.documentai import (  # type: ignore[import]
        DocumentProcessorServiceClient,
    )


logger = logging.getLogger(__name__)


@dataclass
class DocAIParsingResults:
    """A dataclass to store Document AI parsing results."""

    source_path: str
    parsed_path: str


class DocAIParser(BaseBlobParser):
    """`Google Cloud Document AI` parser.

    For a detailed explanation of Document AI, refer to the product documentation.
    https://cloud.google.com/document-ai/docs/overview
    """

    def __init__(
        self,
        *,
        client: Optional["DocumentProcessorServiceClient"] = None,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        gcs_output_path: Optional[str] = None,
        processor_name: Optional[str] = None,
    ) -> None:
        """Initializes the parser.

        Args:
            client: a DocumentProcessorServiceClient to use
            location: a Google Cloud location where a Document AI processor is located
            gcs_output_path: a path on Google Cloud Storage to store parsing results
            processor_name: full resource name of a Document AI processor or processor
                version

        You should provide either a client or location (and then a client
            would be instantiated).
        """

        if bool(client) == bool(location):
            raise ValueError(
                "You must specify either a client or a location to instantiate "
                "a client."
            )

        pattern = r"projects\/[0-9]+\/locations\/[a-z\-0-9]+\/processors\/[a-z0-9]+"
        if processor_name and not re.fullmatch(pattern, processor_name):
            raise ValueError(
                f"Processor name {processor_name} has the wrong format. If your "
                "prediction endpoint looks like https://us-documentai.googleapis.com"
                "/v1/projects/PROJECT_ID/locations/us/processors/PROCESSOR_ID:process,"
                " use only projects/PROJECT_ID/locations/us/processors/PROCESSOR_ID "
                "part."
            )

        self._gcs_output_path = gcs_output_path
        self._processor_name = processor_name
        if client:
            self._client = client
        else:
            try:
                from google.api_core.client_options import ClientOptions
                from google.cloud.documentai import DocumentProcessorServiceClient
            except ImportError as exc:
                raise ImportError(
                    "Could not import google-cloud-documentai python package. "
                    "Please, install docai dependency group: "
                    "`pip install langchain-google-community[docai]`"
                ) from exc
            options = ClientOptions(
                quota_project_id=project_id,
                api_endpoint=f"{location}-documentai.googleapis.com",
            )
            self._client = DocumentProcessorServiceClient(
                client_options=options,
                client_info=get_client_info(module="document-ai"),
            )
            # get processor type
            self._processor_type = self._client.get_processor(name=processor_name).type
            if self._processor_type == "LAYOUT_PARSER_PROCESSOR":
                self._use_layout_parser = True
            else:
                self._use_layout_parser = False

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Parses a blob lazily.

        Args:
            blobs: a Blob to parse

        This is a long-running operation. A recommended way is to batch
            documents together and use the `batch_parse()` method.
        """
        yield from self.batch_parse([blob], gcs_output_path=self._gcs_output_path)

    def online_process(
        self,
        blob: Blob,
        enable_native_pdf_parsing: bool = True,
        field_mask: Optional[str] = None,
        page_range: Optional[List[int]] = None,
        chunk_size: int = 500,
        include_ancestor_headings: bool = True,
    ) -> Iterator[Document]:
        """Parses a blob lazily using online processing.

        Args:
            blob: a blob to parse.
            enable_native_pdf_parsing: enable pdf embedded text extraction
            field_mask: a comma-separated list of which fields to include in the
                Document AI response.
                suggested: "text,pages.pageNumber,pages.layout"
            page_range: list of page numbers to parse. If `None`,
                entire document will be parsed.
            chunk_size: the maximum number of characters per chunk
            include_ancestor_headings: whether to include ancestor headings in the chunks
                https://cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1beta3#chunkingconfig
        """
        try:
            from google.cloud import documentai
            from google.cloud.documentai_v1.types import (  # type: ignore[import, attr-defined]
                OcrConfig,
                ProcessOptions,
            )
        except ImportError as exc:
            raise ImportError(
                "Could not import google-cloud-documentai python package. "
                "Please, install docai dependency group: "
                "`pip install langchain-google-community[docai]`"
            ) from exc
        try:
            from google.cloud.documentai_toolbox.wrappers.page import (  # type: ignore[import]
                _text_from_layout,
            )
        except ImportError as exc:
            raise ImportError(
                "documentai_toolbox package not found, please install it with "
                "`pip install langchain-google-community[docai]`"
            ) from exc

        if self._use_layout_parser:
            layout_config = ProcessOptions.LayoutConfig(
                chunking_config=ProcessOptions.LayoutConfig.ChunkingConfig(
                    chunk_size=chunk_size,
                    include_ancestor_headings=include_ancestor_headings,
                )
            )
            individual_page_selector = (
                ProcessOptions.IndividualPageSelector(pages=page_range)
                if page_range
                else None
            )
            process_options = ProcessOptions(
                layout_config=layout_config,
                individual_page_selector=individual_page_selector,
            )
        else:
            ocr_config = (
                OcrConfig(enable_native_pdf_parsing=enable_native_pdf_parsing)
                if enable_native_pdf_parsing
                else None
            )
            individual_page_selector = (
                ProcessOptions.IndividualPageSelector(pages=page_range)
                if page_range
                else None
            )
            process_options = ProcessOptions(
                ocr_config=ocr_config, individual_page_selector=individual_page_selector
            )

        response = self._client.process_document(
            documentai.ProcessRequest(
                name=self._processor_name,
                gcs_document=documentai.GcsDocument(
                    gcs_uri=blob.path,
                    mime_type=blob.mimetype or "application/pdf",
                ),
                process_options=process_options,
                skip_human_review=True,
                field_mask=field_mask,
            )
        )

        if self._use_layout_parser:
            yield from (
                Document(
                    page_content=chunk.content,
                    metadata={
                        "chunk_id": chunk.chunk_id,
                        "source": blob.path,
                    },
                )
                for chunk in response.document.chunked_document.chunks
            )
        else:
            yield from (
                Document(
                    page_content=_text_from_layout(page.layout, response.document.text),
                    metadata={
                        "page": page.page_number,
                        "source": blob.path,
                    },
                )
                for page in response.document.pages
            )

    def batch_parse(
        self,
        blobs: Sequence[Blob],
        gcs_output_path: Optional[str] = None,
        timeout_sec: int = 3600,
        check_in_interval_sec: int = 60,
        chunk_size: int = 500,
        include_ancestor_headings: bool = True,
    ) -> Iterator[Document]:
        """Parses a list of blobs lazily.

        Args:
            blobs: a list of blobs to parse.
            gcs_output_path: a path on Google Cloud Storage to store parsing results.
            timeout_sec: a timeout to wait for Document AI to complete, in seconds.
            check_in_interval_sec: an interval to wait until next check
                whether parsing operations have been completed, in seconds
        This is a long-running operation. A recommended way is to decouple
            parsing from creating LangChain Documents:
            >>> operations = parser.docai_parse(blobs, gcs_path)
            >>> parser.is_running(operations)
            You can get operations names and save them:
            >>> names = [op.operation.name for op in operations]
            And when all operations are finished, you can use their results:
            >>> operations = parser.operations_from_names(operation_names)
            >>> results = parser.get_results(operations)
            >>> docs = parser.parse_from_results(results)
        """
        output_path = gcs_output_path or self._gcs_output_path
        if not output_path:
            raise ValueError(
                "An output path on Google Cloud Storage should be provided."
            )
        operations = self.docai_parse(
            blobs,
            gcs_output_path=output_path,
            chunk_size=chunk_size,
            include_ancestor_headings=include_ancestor_headings,
        )
        operation_names = [op.operation.name for op in operations]
        logger.debug(
            "Started parsing with Document AI, submitted operations %s", operation_names
        )
        time_elapsed = 0
        while self.is_running(operations):
            time.sleep(check_in_interval_sec)
            time_elapsed += check_in_interval_sec
            if time_elapsed > timeout_sec:
                raise TimeoutError(
                    "Timeout exceeded! Check operations " f"{operation_names} later!"
                )
            logger.debug(".")

        results = self.get_results(operations=operations)
        yield from self.parse_from_results(results)

    def parse_from_results(
        self, results: List[DocAIParsingResults]
    ) -> Iterator[Document]:
        try:
            from google.cloud.documentai_toolbox.utilities.gcs_utilities import (  # type: ignore[import]
                split_gcs_uri,
            )
            from google.cloud.documentai_toolbox.wrappers.document import (  # type: ignore[import]
                _get_shards,
            )
            from google.cloud.documentai_toolbox.wrappers.page import _text_from_layout
        except ImportError as exc:
            raise ImportError(
                "documentai_toolbox package not found, please install it with "
                "`pip install langchain-google-community[docai]`"
            ) from exc
        for result in results:
            print(f"processing: {result.parsed_path}")
            gcs_bucket_name, gcs_prefix = split_gcs_uri(result.parsed_path)
            shards = _get_shards(gcs_bucket_name, gcs_prefix + "/")
            if self._use_layout_parser:
                yield from (
                    Document(
                        page_content=chunk.content,
                        metadata={
                            "chunk_id": chunk.chunk_id,
                            "source": result.source_path,
                        },
                    )
                    for shard in shards
                    for chunk in shard.chunked_document.chunks
                )
            else:
                yield from (
                    Document(
                        page_content=_text_from_layout(page.layout, shard.text),
                        metadata={
                            "page": page.page_number,
                            "source": result.source_path,
                        },
                    )
                    for shard in shards
                    for page in shard.pages
                )

    def operations_from_names(self, operation_names: List[str]) -> List["Operation"]:
        """Initializes Long-Running Operations from their names."""
        try:
            from google.longrunning.operations_pb2 import (  # type: ignore[import]
                GetOperationRequest,
            )
        except ImportError as exc:
            raise ImportError(
                "long running operations package not found, please install it with"
                "`pip install langchain-google-community[docai]`"
            ) from exc

        return [
            self._client.get_operation(request=GetOperationRequest(name=name))
            for name in operation_names
        ]

    def is_running(self, operations: List["Operation"]) -> bool:
        return any(not op.done() for op in operations)

    def docai_parse(
        self,
        blobs: Sequence[Blob],
        *,
        gcs_output_path: Optional[str] = None,
        processor_name: Optional[str] = None,
        batch_size: int = 1000,
        enable_native_pdf_parsing: bool = True,
        field_mask: Optional[str] = None,
        chunk_size: Optional[int] = 500,
        include_ancestor_headings: Optional[bool] = True,
    ) -> List["Operation"]:
        """Runs Google Document AI PDF Batch Processing on a list of blobs.

        Args:
            blobs: a list of blobs to be parsed
            gcs_output_path: a path (folder) on GCS to store results
            processor_name: name of a Document AI processor.
            batch_size: amount of documents per batch
            enable_native_pdf_parsing: a config option for the parser
            field_mask: a comma-separated list of which fields to include in the
                Document AI response.
                suggested: "text,pages.pageNumber,pages.layout"
            chunking_config: Serving config for chunking when using layout
                parser processor. Specify config parameters as dictionary elements.
                https://cloud.google.com/document-ai/docs/reference/rpc/google.cloud.documentai.v1beta3#chunkingconfig

        Document AI has a 1000 file limit per batch, so batches larger than that need
        to be split into multiple requests.
        Batch processing is an async long-running operation
        and results are stored in a output GCS bucket.
        """
        try:
            from google.cloud import documentai
            from google.cloud.documentai_v1.types import OcrConfig, ProcessOptions
        except ImportError as exc:
            raise ImportError(
                "documentai package not found, please install it with "
                "`pip install langchain-google-community[docai]`"
            ) from exc

        output_path = gcs_output_path or self._gcs_output_path
        if output_path is None:
            raise ValueError(
                "An output path on Google Cloud Storage should be provided."
            )
        processor_name = processor_name or self._processor_name
        if processor_name is None:
            raise ValueError("A Document AI processor name should be provided.")

        operations = []
        for batch in batch_iterate(size=batch_size, iterable=blobs):
            input_config = documentai.BatchDocumentsInputConfig(
                gcs_documents=documentai.GcsDocuments(
                    documents=[
                        documentai.GcsDocument(
                            gcs_uri=blob.path,
                            mime_type=blob.mimetype or "application/pdf",
                        )
                        for blob in batch
                    ]
                )
            )

            output_config = documentai.DocumentOutputConfig(
                gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(
                    gcs_uri=output_path, field_mask=field_mask
                )
            )

            if self._use_layout_parser:
                layout_config = ProcessOptions.LayoutConfig(
                    chunking_config=ProcessOptions.LayoutConfig.ChunkingConfig(
                        chunk_size=chunk_size,
                        include_ancestor_headings=include_ancestor_headings,
                    )
                )
                process_options = ProcessOptions(layout_config=layout_config)
            else:
                process_options = (
                    ProcessOptions(
                        ocr_config=OcrConfig(
                            enable_native_pdf_parsing=enable_native_pdf_parsing
                        )
                    )
                    if enable_native_pdf_parsing
                    else None
                )
            operations.append(
                self._client.batch_process_documents(
                    documentai.BatchProcessRequest(
                        name=processor_name,
                        input_documents=input_config,
                        document_output_config=output_config,
                        process_options=process_options,
                        skip_human_review=True,
                    )
                )
            )
        return operations

    def get_results(self, operations: List["Operation"]) -> List[DocAIParsingResults]:
        try:
            from google.cloud.documentai_v1 import (  # type: ignore[import]
                BatchProcessMetadata,
            )
        except ImportError as exc:
            raise ImportError(
                "documentai package not found, please install it with "
                "`pip install langchain-google-community[docai]`"
            ) from exc

        return [
            DocAIParsingResults(
                source_path=status.input_gcs_source,
                parsed_path=status.output_gcs_destination,
            )
            for op in operations
            for status in (
                op.metadata.individual_process_statuses
                if isinstance(op.metadata, BatchProcessMetadata)
                else BatchProcessMetadata.deserialize(
                    op.metadata.value
                ).individual_process_statuses
            )
        ]
    
# @title Custom Cloud Storage Loader

logger = logging.getLogger(__name__)

class CustomGCSDirectoryLoader(GCSDirectoryLoader, BaseLoader):
    def load(self, file_pattern=None) -> List[Document]:
        """Load documents."""
        try:
            from google.cloud import storage
        except ImportError:
            raise ImportError(
                "Could not import google-cloud-storage python package. "
                "Please install it with `pip install google-cloud-storage`."
            )
        client = storage.Client(
            project=self.project_name,
            client_info=get_client_info(module="google-cloud-storage"),
        )

        regex = None
        if file_pattern:
            regex = re.compile(r'{}'.format(file_pattern))

        docs = []
        for blob in client.list_blobs(self.bucket, prefix=self.prefix):
            # we shall just skip directories since GCSFileLoader creates
            # intermediate directories on the fly
            if blob.name.endswith("/"):
                continue
            if regex and not regex.match(blob.name):
                continue
            # Use the try-except block here
            try:
                logger.info(f"Processing {blob.name}")
                temp_blob = Blob(path=f"gs://{blob.bucket.name}/{blob.name}")
                docs.append(temp_blob)
            except Exception as e:
                if self.continue_on_failure:
                    logger.warning(f"Problem processing blob {blob.name}, message: {e}")
                    continue
                else:
                    raise e
        return docs
    

# @title Utility methods for adding index to Vertex AI Vector Search
def get_batches(items: List, n: int = 1000) -> List[List]:
    n = max(1, n)
    return [items[i : i + n] for i in range(0, len(items), n)]


def add_data(vector_store, chunks) -> None:
    if RUN_INGESTION:
        batch_size = 1000
        texts = get_batches([chunk.page_content for chunk in chunks], n=batch_size)
        metadatas = get_batches([chunk.metadata for chunk in chunks], n=batch_size)

        for i, (b_texts, b_metadatas) in enumerate(zip(texts, metadatas)):
            print(f"Adding {len(b_texts)} data points to index")
            is_complete_overwrite = bool(i == 0)
            vector_store.add_texts(
                texts=b_texts,
                metadatas=b_metadatas,
                is_complete_overwrite=is_complete_overwrite,
            )
    else:
        print("Skipping ingestion. Enable `RUN_INGESTION` flag")

        
# Utility methods for displaying rich content results

def get_chunk_content(results: List) -> List:
    return [
        doc.page_content.replace("\n", "<br>")
        + f'<br><br> <b><a href="">Source: {doc.metadata.get("source")}</a></b>'
        for doc in results
    ][:5]


CONTRASTING_COLORS = [
    "rgba(255, 0, 0, 0.2)",  # Semi-transparent red
    "rgba(0, 255, 0, 0.2)",  # Semi-transparent green
    "rgba(0, 0, 255, 0.2)",  # Semi-transparent blue
    "rgba(255, 255, 0, 0.2)",  # Semi-transparent yellow
    "rgba(0, 255, 255, 0.2)",  # Semi-transparent cyan
    "rgba(255, 0, 255, 0.2)",  # Semi-transparent magenta
    "rgba(255, 165, 0, 0.2)",  # Semi-transparent orange
    "rgba(255, 105, 180, 0.2)",  # Semi-transparent pink
    "rgba(75, 0, 130, 0.2)",  # Semi-transparent indigo
    "rgba(255, 192, 203, 0.2)",  # Semi-transparent light pink
    "rgba(64, 224, 208, 0.2)",  # Semi-transparent turquoise
    "rgba(128, 0, 128, 0.2)",  # Semi-transparent purple
    "rgba(210, 105, 30, 0.2)",  # Semi-transparent chocolate
    "rgba(220, 20, 60, 0.2)",  # Semi-transparent crimson
    "rgba(95, 158, 160, 0.2)",  # Semi-transparent cadet blue
    "rgba(255, 99, 71, 0.2)",  # Semi-transparent tomato
    "rgba(144, 238, 144, 0.2)",  # Semi-transparent light green
    "rgba(70, 130, 180, 0.2)",  # Semi-transparent steel blue
]


def convert_markdown_to_html(text: str) -> str:
    # Convert Markdown to HTML, ensuring embedded HTML is preserved and interpreted correctly.
    md_extensions = [
        "extra",
        "abbr",
        "attr_list",
        "def_list",
        "fenced_code",
        "footnotes",
        "md_in_html",
        "tables",
        "admonition",
        "codehilite",
        "legacy_attrs",
        "legacy_em",
        "meta",
        "nl2br",
        "sane_lists",
        "smarty",
        "toc",
        "wikilinks",
    ]
    return str(md.markdown(text, extensions=md_extensions))


# Utility function to create HTML table with colored results
def display_html_table(simple_results: List[str], reranked_results: List[str]) -> None:
    # Find all unique values in both lists
    unique_values = set(simple_results + reranked_results)

    # Ensure we have enough colors for all unique values
    # If not, colors will repeat, which might not be ideal but is necessary if the number of unique values exceeds the number of colors
    colors = CONTRASTING_COLORS * (len(unique_values) // len(CONTRASTING_COLORS) + 1)

    # Create a dictionary to map each unique value to a color
    color_map = dict(zip(unique_values, colors))

    # Initialize the HTML table with style for equal column widths
    html = """
    <style>
    td, th {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        color: #000;
    }
    tr {background-color: #ffffff;}
    /* Set table layout to fixed to respect column widths */
    table {
        table-layout: fixed;
        width: 100%; /* You can adjust the overall table width as needed */
        max-height: 100vh !important; /* Set the maximum height of the table */
        overflow-y: auto; /* Add a vertical scrollbar if the content exceeds the maximum height */
    }
    /* Set equal width for both columns */
    td, th {
        width: 50%;
    }
    .text-black {
        color: #000; /* Set the text color to black */
    }
    </style>
    <table>
    <tr><th>Retriever Results</th><th>Reranked Results</th></tr>
    """
    # Iterate over the results and assign the corresponding color to each cell
    for simple, reranked in zip(simple_results, reranked_results):
        html += f"""
        <tr>
            <td style='color: black; background-color: {color_map[simple]}; font-size: 8px;'>
                <p class='text-black'>{convert_markdown_to_html(simple)}</p>
            </td>
            <td style='color: black; background-color: {color_map[reranked]}; font-size: 8px;'>
                <p class='text-black'>{convert_markdown_to_html(reranked)}</p>
            </td>
        </tr>
        """
    html += "</table>"
    display(HTML(html))


def get_sxs_comparison(
    simple_retriever, reranking_api_retriever, query, search_kwargs
) -> List:
    simple_results = get_chunk_content(
        simple_retriever.invoke(query, search_kwargs=search_kwargs)
    )
    reranked_results = get_chunk_content(
        reranking_api_retriever.invoke(query, search_kwargs=search_kwargs)
    )
    display_html_table(simple_results, reranked_results)

    return reranked_results


def display_grounded_generation(response) -> None:
    # Extract the answer with citations and cited chunks
    answer_with_citations = response.answer_with_citations
    cited_chunks = response.cited_chunks

    # Build HTML for the chunks
    chunks_html = "".join(
        [
            f"<div id='chunk-{index}' class='chunk'>"
            + f"<div class='source'>Source {index}: <a href='{chunk['source'].metadata['source']}' target='_blank'>{chunk['source'].metadata['source']}</a></div>"
            + f"<p>{chunk['chunk_text']}</p>"
            + "</div>"
            for index, chunk in enumerate(cited_chunks)
        ]
    )

    # Replace citation indices with hoverable spans
    for index in range(len(cited_chunks)):
        answer_with_citations = answer_with_citations.replace(
            f"[{index}]",
            f"<span class='citation' onmouseover='highlight({index})' onmouseout='unhighlight({index})'>[{index}]</span>",
        )

    # The complete HTML
    html_content = f"""
    <style>
    .answer-box {{
        background-color: #f8f9fa;
        border-left: 4px solid #0056b3;
        padding: 20px;
        margin-bottom: 20px;
        color: #000;
    }}
    .citation {{
        background-color: transparent;
        cursor: pointer;
    }}
    .chunk {{
        background-color: #ffffff;
        border-left: 4px solid #007bff;
        padding: 10px;
        margin-bottom: 10px;
        transition: background-color 0.3s;
        color: #000;
    }}
    .source {{
        font-weight: bold;
        margin-bottom: 5px;
    }}
    a {{
        text-decoration: none;
        color: #0056b3;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    </style>
    <div class='answer-box'>{answer_with_citations}</div>
    <div class='chunks-box'>{chunks_html}</div>
    <script>
    function highlight(index) {{
        // Highlight the citation in the answer
        document.querySelectorAll('.citation').forEach(function(citation) {{
            if (citation.textContent === '[' + index + ']') {{
                citation.style.backgroundColor = '#ffff99';
            }}
        }});
        // Highlight the corresponding chunk
        document.getElementById('chunk-' + index).style.backgroundColor = '#ffff99';
    }}
    function unhighlight(index) {{
        // Unhighlight the citation in the answer
        document.querySelectorAll('.citation').forEach(function(citation) {{
            if (citation.textContent === '[' + index + ']') {{
                citation.style.backgroundColor = 'transparent';
            }}
        }});
        // Unhighlight the corresponding chunk
        document.getElementById('chunk-' + index).style.backgroundColor = '#ffffff';
    }}
    </script>
    """
    display(HTML(html_content))