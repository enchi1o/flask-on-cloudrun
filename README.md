# Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/enchi1o/flask-on-cloudrun.git
    cd ./flask-on-cloudrun
    ```

2. Install the required dependencies:

    ```bash
    poetry install
    ```

3. Virtual execution environment:

    ```bash
    poetry shell
    ```

4. Start the application:

    ```bash
    python ./app.py
    ```

5. Access the application in your web browser:

    ```bash
    http://localhost:5000
    ```

Note: Make sure you have Python and Poetry installed on your machine before proceeding.

## Deploy on Cloud Run

1. Download gcloud SDK in your system.

2. Sign in to GCP using gcloud.

3. Create a Cloud Storage bucket

4. Create a Cloud SQL instance

5. Create service-accounts using gcloud.

    ```bash
    gcloud iam service-accounts create {SERVICE-ACCOUT-NAME}
    ```

6. Cloud Storage add-iam-policy-binding

    ```powershell
    gcloud projects add-iam-policy-binding {GKE-PROJECT-ID}  `
    --member "serviceAccount:{SERVICE-ACCOUT-NAME}@{GKE-PROJECT-ID}.iam.gserviceaccount.com" `
    --role "roles/storage.objectAdmin" 
    ```

7. Cloud SQL add-iam-policy-binding

    ```powershell
    gcloud projects add-iam-policy-binding {GKE-PROJECT-ID}  `
    --member "serviceAccount:{SERVICE-ACCOUT-NAME}@{GKE-PROJECT-ID}.iam.gserviceaccount.com" `
    --role "roles/cloudsql.client"
    ```

8. Deploy on Cloud Run

    ```powershell
    gcloud run deploy {CLOUD-RUN-NAME} `
    --source . `
    --execution-environment gen2 `
    --allow-unauthenticated `
    --service-account {SERVICE-ACCOUT-NAME} `
    --update-env-vars CLOUDSQL=True `
    --update-env-vars CLOUDSTORAGE=True `
    --update-env-vars BUCKET={CLOUD-STORAGE-BUCKET-NAME} `
    --add-cloudsql-instances {GKE-PROJECT-ID}:{CLOUDSQL-REGION}:{CLOUDSQL-NAME}
    ```
