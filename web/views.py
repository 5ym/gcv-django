from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from google.cloud import vision
import io

class index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    def post(self, request, *args, **kwargs):
        client = vision.ImageAnnotatorClient()
        content = request.FILES.get('file').read()
        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        con = ''
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                con += '\nBlock confidence: {}\n'.format(block.confidence)
                for paragraph in block.paragraphs:
                    con += 'Paragraph confidence: {}'.format(paragraph.confidence)
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        con += 'Word text: {} (confidence: {})'.format(word_text, word.confidence)
                        for symbol in word.symbols:
                            con += '\nSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence)
        context = {
            'response': con,
        }
        return render(request, 'index.html', context)