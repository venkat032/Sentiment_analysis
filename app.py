from openai import OpenAI
from flask import Flask,request,render_template
import pandas as pd

app = Flask(__name__)
csv_file = 'demo.csv'

client = OpenAI(
    api_key='enter your groq api key here',
    base_url='https://api.groq.com/openai/v1'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze',methods=['POST'])
def analyze():
    try:
        sentence = request.form['sentence']
        if not sentence.strip():
            return render_template('index.html',error='please enter a sentence')
        response = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
             {'role':'user','content':f'This prompt is for sentiment analysis (classification). Return only Positive or Negative based on this sentence: {sentence}'}
        ])

        sentiment = response.choices[0].message.content.strip()
        new_entry = pd.DataFrame({'sentence':[sentence],'response':[sentiment]})
        
        try:
            existing_df = pd.read_csv(csv_file)
            updated_df = pd.concat([existing_df,new_entry],ignore_index=True)
        except FileNotFoundError:
            updated_df = new_entry
        updated_df.to_csv(csv_file,index=False)
        return render_template('index.html',sentence=sentence,sentiment=sentiment)
    except Exception as e:
        print('Error during analysis:',str(e))
        return render_template('index.html',error='Something went wrong please try again')
    
if __name__ == '__main__':
    app.run(debug=True)


#code for ai to respond

# response = client.chat.completions.create(
#     model='llama3-8b-8192',
#     messages=[
#         {'role':'user','content':f'this prompt is for sentiment analysis(classification) and you have to return positive or negative based on this sentence {sentence}'}
#     ]

# )

# res = response.choices[0].message.content.lower()
# if 'negative' in res:
#     res='negative'
# else:
#     res='positive'


# import pandas as pd
# df=pd.read_csv('demo.csv')

# data1 = {'sentence':[sentence],'response':[res]}
# df1=pd.DataFrame(data1)

# df2 = pd.concat([df,df1],ignore_index=True)
# print(df2)

# df2.to_csv('demo.csv',index=False)