#include <bits/stdc++.h>
#include <fstream>
using namespace std;

//sortした単語を返す関数
string sort_string(string line){
    sort(line.begin(),line.end());
    return line;
}

//dictionaryの型
struct word{
    string original_word;
    string sorted_word;
};

int main(){
    //辞書のソート
    ifstream words("words.txt");
    string line;
    vector<word> dictionary;
    while(getline(words,line)){
        dictionary.push_back({line,sort_string(line)}); //original,sortの順って分かるようにしたい
    }
    sort(dictionary.begin(),dictionary.end(),[](const struct word& a,const struct word& b){return a.sorted_word<b.sorted_word;});

    //q個の単語が来ることを想定
    int q;cin >> q;
    vector<string> word(q);
    vector<vector<string>> ans_word(q); //まとめて出力
    for(int i=0;i<q;i++){
        cin >> word[i];
    }
    for(int i=0;i<q;i++){
        sort(word[i].begin(),word[i].end()); //文字列のソート

        //二分探索 辞書に入ってない文字列は0を出力
        if(dictionary[0].sorted_word==word[i]){ 
            ans_word[i].push_back(dictionary[i].original_word);
        }else if(dictionary[0].sorted_word<word[i] && word[i]<=dictionary[int(dictionary.size())-1].sorted_word){
            int ng=0,ok=int(dictionary.size())-1;
            while(abs(ng-ok)>1){
                int mid = (ok+ng)/2;
                if(word[i]<=dictionary[mid].sorted_word){
                    ok=mid;
                }else{
                    ng=mid;
                }
            }
            if(word[i]!=dictionary[ok].sorted_word){
                ans_word[i].push_back("0");
            }
            while(word[i]==dictionary[ok].sorted_word){
                ans_word[i].push_back(dictionary[ok].original_word);
                ok++;
            }
        }else{
            ans_word[i].push_back("0");
        }
    }

    //出力
    for(size_t i=0;i<q;i++){
        for(size_t j=0;j<ans_word[i].size();j++){
            cout << ans_word[i][j] << " ";
        }
        cout << "\n";
    }
}

//テストは{6 a aa ab comprehensibility 1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}
//空文字列の場合は単語数にカウントされない