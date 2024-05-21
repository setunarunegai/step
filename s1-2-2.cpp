#include <bits/stdc++.h>
#include <fstream>
using namespace std;

//dictionaryの型
struct WordAndScore{
    int score;
    vector<int> alphabets;
    string original_word;
};

//dictionary[i].original_wordがアナグラムかどうか
bool Contains(vector<int> dictionary_alphabets, vector<int> str_cnt){
    for(int j=0;j<26;j++){
        if(str_cnt[j]<dictionary_alphabets[j]){
            return false;
        }
    }
    return true;
}

int main(){
    //辞書のカウント
    ifstream words("words.txt");
    string line;
    vector<WordAndScore> dictionary;
    vector<int> scores = {1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4};
    vector<int> base_alphabets(26,0);
    while(getline(words,line)){
        dictionary.push_back({0,base_alphabets,line}); //{要素の値0が26個}==string(0,26)
    }
    for(size_t i=0;i<dictionary.size();i++){
        for(size_t j=0;j<dictionary[i].original_word.size();j++){
            dictionary[i].alphabets[dictionary[i].original_word[j]-'a']++;
            dictionary[i].score+=scores[dictionary[i].original_word[j]-'a'];
        }
    }
    sort(dictionary.begin(),dictionary.end(),[](const struct WordAndScore& a,const struct WordAndScore& b){return a.score>b.score;});

    //もっともスコアの高い文字列を列挙したtxtを出力
    auto findbestscore = [&](string input,string output){
        ifstream ifs(input);
        ofstream ofs(output);
        while(getline(ifs,line)){
            vector<int> str_cnt(26,0);
            for(size_t i=0;i<line.size();i++){
                str_cnt[line[i]-'a']++;
            }
            for(size_t i=0;i<dictionary.size();i++){
                if(Contains(dictionary[i].alphabets,str_cnt)){
                    ofs << dictionary[i].original_word << "\n";
                    break;
                }
            }
        }
    };

    findbestscore("small.txt","small_answer.txt");
    findbestscore("medium.txt","medium_answer.txt");
    findbestscore("large.txt","large_answer.txt");

}