# Introduction, Well-formed XML



## Extensible Markup Language (XML)
- Tagged elements (nested)
- Attributes
  - Each element may have within its opening tag a set of attributes
  - Consist of an attribute name, the equal sign, and then an attribute value
  - Any element can have any number of attributes as long as the attribute names are unique
- Text
  - If XML is thought of as a tree, the text (strings) are the leaf elements of the tree


### Extensible Markup Language (XML) Sample
```XML
<!-- Bookstore with no DTD -->
<Bookstore>
  <Book ISBN="ISBN-0-13-713526-2" Price="85" Edition="3rd">
    <Title>A First Course in Database Systems</Title>
    <Authors>
      <Author>
        <First_Name>Jeffrey</First_Name>
        <Last_Name>Ullman</Last_Name>
      </Author>
      <Author>
        <First_Name>Jennifer</First_Name>
        <Last_Name>Widom</Last_Name>
      </Author>
    </Authors>
  </Book>
  <Book ISBN="ISBN-0-13-815504-6" Price="100">
    <Remark>
      Buy this book bundled with "A First Course" - a great deal!
    </Remark>
    <Title>Database Systems: The Complete Book</Title>
    <Authors>
      <Author>
        <First_Name>Hector</First_Name>
        <Last_Name>Garcia-Molina</Last_Name>
      </Author>
      <Author>
        <First_Name>Jeffrey</First_Name>
        <Last_Name>Ullman</Last_Name>
      </Author>
      <Author>
        <First_Name>Jennifer</First_Name>
        <Last_Name>Widom</Last_Name>
      </Author>
    </Authors>
  </Book>
</Bookstore>
```

