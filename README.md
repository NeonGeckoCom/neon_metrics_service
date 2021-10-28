# NeonAI Metrics Service
Handles client reported metrics and aggregates data for analysis.

## Request Format
Reported metrics should be in the form of a dictionary. The only required parameter is `name`, any other arbitrary data 
may be included in the request.

>Example Request:
>```json
>{
>  "name": "Metric Name",
>  "arbitrary_data": {},
>  "other_param": "data"
>}
>```

## Response Format
No response is expected.

## Docker Configuration
When running this as a docker container, the path to configuration files should be mounted to `/config`.

For example, if your configuration resides in `~/.config`:
```shell
docker run -v /home/$USER/.config:/config -v /home/neon_metrics:/metrics neon_metrics_service
```
