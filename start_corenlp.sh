set -e
cd /Users/davidwiner/documents/stanfordcorenlp

java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000 -parse.extradependencies