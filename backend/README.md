## Folder Structure
Yes everything is in root
```markdown
project_root/
├── app/                        # Empty
├── azure_functions.py          # Azure Functions
├── cloudflare_functions.py     # Cloudflare Workers
├── cron_functions.py           # Cron Jobs
├── main.py                     # FastAPI
├── README.md                   # Project documentation
├── recall_rss.py               # RSS Feed
├── redis_functions.py          # Redis
├── redis_schema.yaml           # Redis Schema
└── requirements.txt            # Python dependencies
```
## How to Run
- Create a `.env` file with following content
```env
AZURE_API_KEY=<AZURE_API_KEY>
AZURE_ENDPOINT=<AZURE_ENDPOINT>
CLOUDFLARE_API_KEY=<CLOUDFLARE_API_KEY>
CLOUDFLARE_ACCOUNT_ID=<CLOUDFLARE_ACCOUNT_ID>
CLOUDFLARE_BASE_URL=<CLOUDFLARE_BASE_URL>
REDIS_URL=<REDIS_URL>
DISCORD_WEBHOOK=<DISCORD_WEBHOOK>
AZURE_BLOB_API_KEY=<AZURE_BLOB_API_KEY>
AZURE_BLOB_ENDPOINT=<AZURE_BLOB_ENDPOINT>
```
- Install dependencies `pip install -r requirements.txt`
- Run `uvicorn main:app  --reload --host 0.0.0.0 --port 8080`
- Send POST request to `http://localhost:8080/` according to documentation
****
### cron Job
- To run cron job, run `python cron_function.py`
## Documentation
- After server is running, documentation is available at `http://localhost:8080/docs`
- POSTMAN collection is also available at `https://documenter.getpostman.com/view/25806974/2s9YyvCM3d`