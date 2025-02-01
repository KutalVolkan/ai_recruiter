## Get Started

Set the environment variables in `.env` as needed:

```bash
$ cp .env.example .env
```

### Run All-in-One Command

> **Note:** The `resume_generator` service can take a really long time to run. If you don't need to generate new resumes and would rather use the provided example CVs from `resume_collection`, consider running the services separately (steps 1 and 3) instead.

```bash
$ cp .env.example .env
$ docker-compose build && docker-compose run resume_generator && docker-compose run ai_recruiter
```

### Alternatively, Run Commands Separately

If you prefer to run the services step-by-step for more control or want to avoid the lengthy resume generation process, follow these steps:

1. **Build the Docker images:**
   ```bash
   $ docker-compose build
   ```

2. **(Optional) Run the `resume_generator` to create resumes:**

   > **Note:** This step can take a long time to complete. If you'd like to use the example CVs provided in `resume_collection`, you can skip this step.

   ```bash
   $ docker-compose run resume_generator
   ```

3. **Run the `ai_recruiter` service to evaluate candidates:**
   ```bash
   $ docker-compose run ai_recruiter
   ```