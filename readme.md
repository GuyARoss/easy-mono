## Easy Mono Mirror
Easy mono mirror is a program that manages a mirror of micro repositories as a single mono repository. Made with githooks in mind.

### Requirements
- Python (2.7)
- Golang

### Usage (without docker)
First install dependencies from `requirements.txt` (__note__ we are using 2.7.16 here).

Next, please ensure that your git profile is correctly configured on your machine.

Lastly, update the `manifest.json` with your mono settings. To run, start the application with `go run`.

### Manifest Instructions
The manifest contains 3 primary properties `remote`, `projects` & `schema`. 
- Remote: A single string that includes that remote address for the mono repository.
- Projects: An array of objects where that object includes `key`, `shallow` & `url`.  
    - Key: String identifier you want to be associated with a particular repo.
    - Shallow: Boolean that determines if this project should be in dumped in root level of a particular folder structure.
    - Url: Project remote as string
- Schema: array of either objects or strings that determine the folder structure of the mono repo.

E.g
```json
{
	"remote": "http://some-remote-address.com",
	"projects": [
		{ "key": "project-1","shallow": false, "url": "http://project-1.remote.com" },
		{ "key": "project-2","shallow": false, "url": "http://project-2.remote.com" },
		{ "key": "project-2.5","shallow": false, "url": "http://project-2.5.remote.com" },
		{ "key": "project-3","shallow": true, "url": "http://project-3.remote.com" },
	],
	"schema": [
		"project-1",
        { "project-2": ["project-2", "project-2.5"]}
	]
}
```
will output the folder structure of
```
- project-1
- project-2
    - project-2.5
- contents of folder 3
```

