class TextPostprocessor:
    def __init__(self):
        pass

    def remove_line_breaks(self, text):
        """
        Remove line breaks from text.
        """
        return text.replace('\n', ' ')

    def capitalize_sentences(self, text):
        """
        Capitalize the first letter of each sentence.
        """
        sentences = text.split('. ')
        sentences = [sentence.capitalize() for sentence in sentences]
        return '. '.join(sentences)

    def extract_info(self, text, keyword):
        """
        Extract information related to a specific keyword from the text.
        """
        sentences = text.split('. ')
        related_sentences = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
        return '. '.join(related_sentences)

    def postprocess(self, text, keyword=None):
        """
        Apply all postprocessing steps to the text.
        """
        text = self.remove_line_breaks(text)
        text = self.capitalize_sentences(text)
        if keyword:
            text = self.extract_info(text, keyword)
        return text

if __name__ == '__main__':
    # Initialize the TextPostprocessor
    postprocessor = TextPostprocessor()

    # Sample text to postprocess
    sample_text = "here is some text. it has multiple sentences. we want to extract information about 'text'."

    # Apply postprocessing
    processed_text = postprocessor.postprocess(sample_text, keyword="text")

    # Display the postprocessed text
    print(processed_text)