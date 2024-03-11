import json
import os

def fetch_content(module_num, topic_num, page_num):
    try:
        print(f"Fetching content for: Module {module_num}, Topic {topic_num}, Page {page_num}")
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        print(f"Folder path: {folder_path}")
        
        # Load the JSON file corresponding to the module number
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        print(f"File path: {file_path}")
        with open(file_path, "r") as file:
            data = json.load(file)
            print(data)
        
        # Retrieve the content based on the specified module, topic, and page numbers
        module = data["modules"][module_num - 1] 
        topic = module["topics"][topic_num - 1]   
        
        title = topic.get('title', 'Default Title')
        narrative = topic.get('narrative', 'Default Narrative')
        
        page = topic["pages"][page_num - 1]  # Adjust index to 0-based
        
        # Return the content
        content = {
            'title': title,
            'narrative': narrative,
            'content': page.get('content', 'Default Content')
        }
        print("Content retrieved successfully.")
        return content
        
    except FileNotFoundError:
        error_msg = "Module not found."
        print(f"Error: {error_msg}")
        return {"error": error_msg}
    except IndexError:
        error_msg = "Topic or page not found."
        print(f"Error: {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(f"Error: {error_msg}")
        return {"error": error_msg}


result= fetch_content(1,1,1)
print(result)
result = fetch_content(2,1,1)
print(result)
result = fetch_content(3,1,1)
print(result)
result = fetch_content(4,1,1)
print(result)
result = fetch_content(5,1,1)
print(result)


def next_page_func(module_num, topic_num, page_num):
    # Load the JSON file corresponding to the module number
    file_path = os.path.join("CourseContent", f"Module{module_num}.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    # Retrieve the number of topics and pages in the current module and topic
    num_topics = len(data["modules"][module_num - 1]["topics"])
    num_pages = len(data["modules"][module_num - 1]["topics"][topic_num - 1]["pages"])

    # Check if there are more pages in the current topic
    if page_num < num_pages:
        return module_num, topic_num, page_num + 1
    else:
        # Check if there are more topics in the current module
        if topic_num < num_topics:
            return module_num, topic_num + 1, 1  # Move to the next topic
        else:
            # Check if there are more modules
            if module_num < len(data["modules"]):
                return module_num + 1, 1, 1  # Move to the next module
            else:
                # Reached the end of the content, reset to the first page of the first topic of the first module
                return 1, 1, 1

def prev_page_func(module_num, topic_num, page_num):
    # Load the JSON file corresponding to the module number
    file_path = os.path.join("CourseContent", f"Module{module_num}.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    # Retrieve the number of topics and pages in the current module and topic
    num_topics = len(data["modules"][module_num - 1]["topics"])
    num_pages = len(data["modules"][module_num - 1]["topics"][topic_num - 1]["pages"])

    # Check if it's the first page
    if page_num == 1:
        # Check if it's the first topic
        if topic_num == 1:
            # Check if it's the first module
            if module_num == 1:
                # Already at the first page of the first topic of the first module
                # Wrap around to the last page of the last topic of the last module
                last_module = len(data["modules"])
                last_topic = len(data["modules"][last_module - 1]["topics"])
                last_page = len(data["modules"][last_module - 1]["topics"][last_topic - 1]["pages"])
                return last_module, last_topic, last_page
            else:
                # Move to the last page of the previous module
                prev_module = module_num - 1
                last_page = len(data["modules"][prev_module - 1]["topics"][-1]["pages"])
                return prev_module, num_topics, last_page
        else:
            # Move to the last page of the previous topic
            prev_topic = topic_num - 1
            last_page = len(data["modules"][module_num - 1]["topics"][prev_topic - 1]["pages"])
            return module_num, prev_topic, last_page
    else:
        # Move to the previous page
        return module_num, topic_num, page_num - 1


def is_module_completed(module_num, topic_num, page_num):
    # Load the JSON file corresponding to the module number
    file_path = os.path.join("CourseContent", f"Module{module_num}.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    # Retrieve the number of topics and pages in the current module
    num_topics = len(data["modules"][module_num - 1]["topics"])
    last_topic_index = num_topics - 1

    # Check if it's the last topic
    if topic_num == num_topics:
        # Retrieve the number of pages in the last topic
        num_pages = len(data["modules"][module_num]["topics"][last_topic_index]["pages"])

        # Check if it's the last page of the last topic
        if page_num == num_pages:
            return True
    
    return False

def fetch_pages_topic(module_num, topic_num):
    try:
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        
        # Load the JSON file corresponding to the module number
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        
        # Retrieve the topics for the specified module
        module = data["modules"][module_num]  # Adjust index to 0-based
        topic = module["topics"][topic_num - 1]  # Adjust index to 0-based
        
        # Calculate and return the total number of pages for the topic
        total_pages = len(topic["pages"])
        return total_pages
        
    except FileNotFoundError:
        print("Error: Module not found.")
        return 0
    except IndexError:
        print("Error: Topic not found.")
        return 0
    except Exception as e:
        print(f"Error: An error occurred: {e}")
        return 0

