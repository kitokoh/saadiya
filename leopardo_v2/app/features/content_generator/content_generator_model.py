import pandas as pd

class ContentGeneratorModel:
    def __init__(self):
        self.contents = pd.DataFrame(columns=["id", "topic", "content_type", "generated_content"])
        self.next_id = 1

    def generate_content(self, topic, content_type):
        # In a real application, this would involve a call to a language model (e.g., GPT)
        generated_content = f"This is a generated {content_type} about '{topic}'."
        new_content = {
            "id": self.next_id,
            "topic": topic,
            "content_type": content_type,
            "generated_content": generated_content
        }
        self.contents = pd.concat([self.contents, pd.DataFrame([new_content])], ignore_index=True)
        self.next_id += 1
        return generated_content

    def get_all_contents(self):
        return self.contents
