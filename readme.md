#downloader

> Docker stack for downloading images and text content of websites

This project offers a RESTful API to download, check status and download images and text content from websites.
When a new website is scheduled for download, the application starts downloading resources in the background.


## Instalation

Download the project, open text console, go to the main folder and run `docker-compose`:

```sh
docker-compose up --build
```

Docker will pull images and start the stack.

## Example usage

Make sure `docker-compose` is running the project.

Use `curl` to create new download job (see `curl.txt` for complete, copy-paste ready commands):
```sh
REQUEST:
POST http://localhost:8080/api/v1/job
POST body: {"type": "text", "url": "https://www-eng-x.llnl.gov/documents/tests/html.html"} 

RESPONSE:
HTTP/1.1 201 CREATED
...
Location: /api/v1/job/08d70736381d488ec22846069388b68b
```

The `Location:` header shows the link to newly created retreieve job.

You can also do a `{"type": "images", "url": "https://www-eng-x.llnl.gov/documents/tests/html.html"}` request.

## Monitoring

You can go to <http://localhost:8081> to see `rq-dasboard` console for GUI based monitor of workers and tasks or you can monitor the status of a job with the following command:

```sh
REQUEST:
GET http://localhost:8080/api/v1/job/08d70736381d488ec22846069388b68b

RESPONSE:
{"status": "pending"}
```
where jobid `08d70736381d488ec22846069388b68b` is taken from location header above.

After a while of re-running this command the status will change from `"pending"` to `"done"`.
Then you can get the downloaded resources:

- Text job:

```sh
Text job example
REQUEST:
GET http://localhost:8080/api/v1/job/08d70736381d488ec22846069388b68b/resources

{
  "status": "done",
  "data": [
    {
        "type": "url",
        "value": "https://www-eng-x.llnl.gov/documents/tests/html.html"
    }, 
    {
        "type": "jobtype",
        "value": "text"
    }, 
    {
        "type": "text"
        "content": "[...]",
    }
  ] 
}
```

- Images job:

```sh
REQUEST:
GET http://localhost:8080/api/v1/job/ec9024e6e143ec4ecbd8eb16b317ebab/resources

{
  "status": "done",
  "data": [
    {
        "type": "url",
        "value": "https://www-eng-x.llnl.gov/documents/tests/html.html"
    }, 
    {
        "type": "jobtype",
        "value": "images"
    }, 
    {
      "type": "image", 
      "value": "data:image/gif;base64,R0lGOD [...] QYCQA7"
    }
  ] 
}
```


## Testing

Start the stack with `docker-compose up --build` and then run `run_tests.sh`


## Author

wpozar@gmail.com
