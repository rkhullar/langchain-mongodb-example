## Objective
Walk through the following tutorial on getting started with semantic search using LangChain and MongoDB:
- https://www.mongodb.com/developer/languages/python/semantic-search-made-easy-langchain-mongodb
- https://github.com/mongodb-developer/atlas-langchain.git

### Tool Versions
- python 3.11.7

### Virtual Environment
- create virtual environment for local development
```shell
./setup-venv.sh
```
- install additional libraries
```shell
pipenv install {library}
```

### Instructions

#### Prerequisites
- MongoDB Account
- AWS Account
- OpenAI API Key

#### Environment Config
```shell
cp .envrc.dist .envrc
cp local.env.dist local.env
# review and update values
# use aws profile as atlas database user
```

#### Load Transform Embed and Store
```shell
python vectorize.py
```
The script takes the wikipedia page for MongoDB and processes it. The content is broken down into sections like paragraphs
or sentences. Each piece of content is then fed through the large language model (LLM) and converted into a large array
of numbers ranging from -1.0 to 1.0. There were around 1500 dimensions using the OpenAI embedding. The results are stored in
MongoDB Atlas and indexed via Atlas Search.

#### Query
The `SearchClient` class within `query.py` can be used to interface with the trained AI model. When text is fed into the
query it would be vectorized and matched against the training data to find an answer. And the LLM should further improve
the response.
```shell
python query_test.py
```
