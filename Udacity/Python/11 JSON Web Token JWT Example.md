# JSON Web Token = JWT

A JSON Web Token (JWT) is a self-contained **JSON object** that **compactly and securely transmits information** between 2 parties. 
It is **digitally signed using a secret or a public/private key pair**.
It is often **sent in the Authorization header using the Bearer schema**, as shown in the code example.
```
Authorization: Bearer abcdeERTfg3.abcdeferrthdfvcsdcERGEWREWR.3B-EWsdfsdfewrDQ3OCw8_mwM
```

## JWT Composition
A JSON Web Token (JWT) consists of:
- A Header
- A Payload
- A Signature
The header and payload will be Base64UrL encoded, and then **each part is separated by a `.`**, which looks like: `encodedHeader.encodedPayload.signature`

### JWT Header
The JWT header contains:
- The type “JWT”
- The hashing algorithm used
Hashing algorithms might be something like HMAC SHA256 or RSA.
```
{
    “alg” : “HS256”
    “typ” : “JWT”
}
```


### JWT Payload
A JWT Payload contains reserved, public, or private statements about the entity (aka “claims”).
- **Reserved Claims** are **predefined** claims.
- **Public Claims** are **defined by a developer** and should be **defined in the IANA JSON WEB Token Registry to avoid collisions**. https://www.iana.org/assignments/jwt/jwt.xhtml
- **Private Claims** are **custom** claims created to **share information between 2 consenting parties**.
```
{   
  "sub": "134567",   
  "name": "Jon Doe",   
  "field3": false 
}
```


### JWT Signature
A JWT Signature, as shown in the code block, is created from the 
- encoded header,
- encoded payload, and
- a secret
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

