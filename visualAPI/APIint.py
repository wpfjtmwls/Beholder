import json
import os
from watson_developer_cloud import VisualRecognitionV3

THRESHOLD = 0.8
UPLOAD_FOLDER = 'data'


def similarity_score(path_name):
    visual_recognition = VisualRecognitionV3('2016-05-20', api_key='ca68de255b014db50da15608d130ac73992ebdc5')
    face_path = os.path.join(UPLOAD_FOLDER, path_name)
    with open(face_path, 'rb') as image_file:
        result = visual_recognition.find_similar(collection_id="bluehackckcck_e296cf", image_file=image_file)
        count = 0
        for x in range(len(result["similar_images"])):
            if result["similar_images"][count]["score"] > THRESHOLD:
                return 1    
            count+=1
        return 0 
    #print(result["similar_images"][0]["score"])
