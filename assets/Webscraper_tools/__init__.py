import importlib_resources

my_resources = importlib_resources.files("Webscraper_tools")
prompt = my_resources.joinpath("Prompt.txt").read_bytes().decode("utf-8")
single_article_summary_prompt = my_resources.joinpath("Single_Article_Prompt.txt").read_bytes().decode("utf-8")