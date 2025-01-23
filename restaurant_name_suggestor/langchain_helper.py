from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret_key import openapi_key

import os
os.environ['OPENAI_API_KEY'] = openapi_key

pre_built_llm = OpenAI(temperature = 0.7) # temparature is level of creativity (0-1)

def generate_restaurant_name_and_items(cuisine):
    # Chain 1: Generate restaurant name
    res_name_template = PromptTemplate(
        input_variables=['cuisine'],
        template = "I want to open a {cuisine} restaurant. Suggest a single fancy name"
    )

    res_name_chain = LLMChain(llm = pre_built_llm, prompt = res_name_template, output_key = "restaurant_name")

    # Chain 2: Generate menu items based on restaurant name
    res_menu_template = PromptTemplate(
        input_variables=['restaurant_name'],
        template = "Suggest some menu items for {restaurant_name}. No need of description of food."
    )

    res_menu_chain = LLMChain(llm = pre_built_llm, prompt = res_menu_template, output_key = "menu_items")

    # Sequential Chain: Combine both chains
    final_chain = SequentialChain(
        chains = [res_name_chain, res_menu_chain],
        input_variables = ['cuisine'],
        output_variables = ['restaurant_name', 'menu_items']
    )

    response = final_chain({'cuisine': cuisine})

    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Italian"))