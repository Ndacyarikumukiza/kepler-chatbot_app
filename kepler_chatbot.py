{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "6c132c87-77fd-4e33-b1ed-e3aed28c5014",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Setup completed in folder 'kepler_chatbot'.\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "\n",
    "# Create folder\n",
    "folder_name = 'kepler_chatbot'\n",
    "os.makedirs(folder_name, exist_ok=True)\n",
    "\n",
    "# Convert Excel to CSV\n",
    "excel_path = r\"D:\\Computer Application\\Chatbot Questions & Answers (1).xlsx\"\n",
    "data = pd.ExcelFile(excel_path)\n",
    "all_data = pd.DataFrame()\n",
    "\n",
    "for sheet in data.sheet_names:\n",
    "    df = data.parse(sheet)\n",
    "    if not df.empty and 'Questions' in df.columns and 'Answers' in df.columns:\n",
    "        all_data = pd.concat([all_data, df[['Questions', 'Answers']]], ignore_index=True)\n",
    "\n",
    "all_data = all_data.dropna(subset=['Questions', 'Answers'])\n",
    "all_data = all_data[all_data['Answers'] != '']\n",
    "all_data = all_data.drop_duplicates(subset=['Questions'], keep='first')\n",
    "\n",
    "csv_path = os.path.join(folder_name, 'questions_answers.csv')\n",
    "all_data.to_csv(csv_path, index=False)\n",
    "\n",
    "# Create app.py file inside the folder\n",
    "with open(os.path.join(folder_name, 'app.py'), 'w') as f:\n",
    "    f.write(\"\"\"\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "\n",
    "data = pd.read_csv('questions_answers.csv')\n",
    "qa_dict = dict(zip(data['Questions'].str.lower(), data['Answers']))\n",
    "\n",
    "def preprocess_question(question):\n",
    "    question = question.lower().strip()\n",
    "    question = question.replace('?', '').replace(\"'\", '').replace('\"', '')\n",
    "    question = question.replace('what', '').replace('how', '').replace('can', '')\n",
    "    question = question.replace('does', '').replace('kepler', '').replace('college', '')\n",
    "    return ' '.join(question.split())\n",
    "\n",
    "def find_best_match(user_question, questions):\n",
    "    user_question = preprocess_question(user_question)\n",
    "    if user_question in questions:\n",
    "        return user_question\n",
    "    for q in questions:\n",
    "        if user_question in q or q in user_question:\n",
    "            return q\n",
    "    user_words = set(user_question.split())\n",
    "    max_overlap = 0\n",
    "    best_match = None\n",
    "    for q in questions:\n",
    "        q_words = set(q.split())\n",
    "        overlap = len(user_words.intersection(q_words))\n",
    "        if overlap > max_overlap:\n",
    "            max_overlap = overlap\n",
    "            best_match = q\n",
    "    return best_match if max_overlap >= 2 else None\n",
    "\n",
    "st.title(\"Kepler College Chatbot\")\n",
    "question = st.text_input(\"Ask me anything about Kepler College\")\n",
    "if question:\n",
    "    user_question_processed = preprocess_question(question)\n",
    "    questions = list(qa_dict.keys())\n",
    "    answer = \"I'm sorry, I don't have information about that.\" \n",
    "    if user_question_processed in questions:\n",
    "        answer = qa_dict[user_question_processed]\n",
    "    else:\n",
    "        best_match = find_best_match(user_question_processed, questions)\n",
    "        if best_match:\n",
    "            answer = qa_dict[best_match]\n",
    "    st.write(answer)\n",
    "\"\"\")\n",
    "\n",
    "# Create requirements.txt file for your project\n",
    "with open(os.path.join(folder_name, 'requirements.txt'), 'w') as f:\n",
    "    f.write('streamlit\\npandas\\n')\n",
    "\n",
    "print(f\"Setup completed in folder '{folder_name}'.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1cff54c7-6552-4ba7-b3e9-8f64b1c03353",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
