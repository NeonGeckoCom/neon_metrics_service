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
When running this as a docker container, the path to configuration files should be mounted to `/config` and the path to
save reported metrics mounted to `/metrics`. This container expects `mq_config.json` to contain service `neon_metrics_connector`.

For example, if your configuration resides in `~/.config` and you want metrics saved to `~/neon_metrics`:
```shell
export CONFIG_PATH="/home/${USER}/.config"
export METRIC_PATH="/home/${USER}/neon_metrics"
docker run -v ${CONFIG_PATH}:/config -v ${METRIC_PATH}:/metrics neon_metrics_service
```
