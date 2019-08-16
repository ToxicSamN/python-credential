# python-credential

## Purpose:
The purpose of this API is to provide a central point in which a user can obtain username/password credentials through code. It is a common issue when coding against systems that require authentication that the credentials have to be provided either via a text file or hard coded into the source code. For obvious reasons this is a bad idea. Storing the files in an encrypted manner on a systems filesystem works great and is what appears to be the accepted method. This can be a headache depending on how many systems you have and have to maintain passwd files over multiple systems. This API is aimed at preventing this and keeping a single source of truth for code project that require credentials. This also separates the confidential data from the system running the code.



## How it Works (High Level):
It works based off of RSA key-pair encryption. A client id must be generated for each system/code/project that requires access to the API. They must also provide their RSA public key when they register the system in the database.

When a credential is stored into the database the API system will encrypt the password with its own public key. When a request comes in for a credential there are some checks in the background looking to ensure a specific client has access to the credential being requested. If the checks all clear then the credentials are decrypted by the API system and re-encrypted with AES and auto generatesd AES KEY. The AES key is then encrypted with the the client's public key and sent back as an http response with a JSON payload. It is up to the user to decrypt the AES KEY and use the the decrypted AES KEY to decrypt the credentials. This is all done over HTTPS as well in order to keep everything from being clear text. The passwords are stored in the database with encryption at rest.

# Usage:
## Prerequisites:
In order for a project to use this API there must be a few things that are setup and registered prior. 
-RSA Public/Private Key pair
-ClientId (Auto Generated)
-Project/System Name
-A List of Username(s)/passwords to store in the database

## RSA Public/Private Key Pair:
Every project will require a new RSA Key Pair. Always keep your private key file protected and secured. The API only works by encrypting the passwords with the project's public key. If the public key provided is wrong or the incorrect public key then the project will not be able to decrypt the password. There are many documents and ways of creating a key pair. This document will show an example way of creating this pair but is by no means the only way to do so.
```
# Generating a private key file using aes128 at 2048 bits (aes256 doesn't work in python module pycryptodome
openssl genrsa -aes128 -out private.pem 2048
 
Generating RSA private key, 2048 bit long modulus
..................+++
.....................................................................................................................................................................................................+++
e is 65537 (0x10001)
 
Enter pass phrase for private.pem: < Provide a Complex Passphrase here but remember it! >
Verifying - Enter pass phrase for private.pem: < Provide a Complex Passphrase here but remember it! >
 
 
# Generate the Public Key File using the Private Key
openssl rsa -aes128 -in private.pem -outform PEM -pubout -out public.pem
 
 
# Prompted to enter the passphrase entered for the key file
Enter pass phrase for private.pem: < Provide a Complex Passphrase here but remember it! >
writing RSA key
 
 
# There should now be a public.pem and a private.pem file generated
ls -lh
total 8.0K
-rw-r--r--. 1 root root 1.8K Aug 15 12:17 private.pem
-rw-r--r--. 1 root root  451 Aug 15 12:17 public.pem
```

## Generate a New ClientId:
NOTE: This assumes you deployed the credstore to a server that resolves to 'credstore'
Open a browser and go to the url https://credstore/credentialstore/NewClientId 


# API Documentation
All URL patterns are Case Sensitive. 

## API Root URL:
This is the root URL for all commands.

https://credstore/credentialstore

## NewClientId
Generates a new client id

### HTTP request
```GET {root_url}/NewClientId```


HTTP Response: ```{ 
    "ClientId" : "string" , 
}```

## GetCredential
Retrieves a username and encrypted password credential.

### HTTP request
```GET {root_url}/GetCredential?ClientId={ClientID}&username={username}```

HTTP Response: ```
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"secret" : [ 
{ 
"username" : "string" , 
"password" : "encrypted password" , 
"shared_key" : "encrypted AES Key" , 
}, 
] 
}```

## CreateClient
Not an Enabled Feature yet.

## UpdateClient
Not an Enabled Feature yet.

## AdminGetAllClients
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves all client information including which username/passwords each client has access to.

### HTTP request
```GET {root_url}/admin/GetAllClients```

HTTP Response: ```
[ 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"secret" : [ 
{ 
"username" : "string" , 
"password" : "encrypted password" , 
}, 
] 
}, 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"secret" : [ 
{ 
"username" : "string" , 
"password" : "encrypted password" , 
}, 
] 
}, 
]```

## AdminGetAllSecrets
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves all Username/Password credentials information.

### HTTP request
```GET {root_url}/admin/GetAllSecrets```

HTTP Response: ```
[ 
{ 
"username" : "string" , 
"password" : "encrypted string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
}, 
{ 
"username" : "string" , 
"password" : "encryptedstring" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
},
]```

## AdminGetClient
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves a specific client information including which username/passwords the client has access to.

### HTTP request
```GET {root_url}/admin/GetClient?ClientId={ClientId}```

HTTP Response: ```
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"secret" : [ 
{ 
"username" : "string" , 
"password" : "encrypted password" , 
}, 
{ 
"username" : "string" , 
"password" : "encrypted password" , 
}, 
] 
}```

## AdminGetSecret
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves a Username/Password credential.

### HTTP request
```GET {root_url}/admin/GetSecret?username={username}```

HTTP Response: ```
{ 
"username" : "string" , 
"password" : "encrypted string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
},```

## AdminGetSecretClients
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves all or a specifc username/password credential including which clients have access to the credential.

### HTTP request
```GET {root_url}/admin/GetSecretClients```

(Optional)

```GET {root_url}/admin/GetSecretClients?username={username} ```

HTTP Response: ```
[ 
{ 
"username" : "string" , 
"clients" : "[" 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"name" : "string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
}, 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"name" : "string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
},
] 
},
{ 
"username" : "string" , 
"clients" : "[" 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"name" : "string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
}, 
{ 
"ClientId" : "string" , 
"pubkey" : "string" , 
"name" : "string" , 
"date_created" : "date/time stamp" , 
"date_modified" : "date/time stamp" , 
},
] 
}, 
]```

## AdminDeleteClient
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves all client information including which username/passwords each client has access to.

### HTTP request
``DELETE {root_url}/admin/DeleteClient?ClientId={ClientId}``


## AdminDeleteSecret
Admin feature only. Must be logged in with an admin enabled user account.

Retrieves all client information including which username/passwords each client has access to.

### HTTP request
```GET {root_url}/admin/DeleteSecret?username={username}```