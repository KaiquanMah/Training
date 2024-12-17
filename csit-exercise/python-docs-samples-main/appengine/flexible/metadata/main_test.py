# Copyright 2023 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    external_ip = main.get_external_ip()

    r = client.get("/")
    assert r.status_code == 200
    assert f"External IP: {external_ip}" in r.data.decode("utf-8")
