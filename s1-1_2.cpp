#include <bits/stdc++.h>
#include <fstream>
using namespace std;

//sort�����P���Ԃ��֐�
string sort_string(string line){
    sort(line.begin(),line.end());
    return line;
}

//dictionary�̌^
struct word{
    string original_word;
    string sorted_word;
};

int main(){
    //�����̃\�[�g
    ifstream words("words.txt");
    string line;
    vector<word> dictionary;
    while(getline(words,line)){
        dictionary.push_back({line,sort_string(line)}); //original,sort�̏����ĕ�����悤�ɂ�����
    }
    sort(dictionary.begin(),dictionary.end(),[](const struct word& a,const struct word& b){return a.sorted_word<b.sorted_word;});

    //q�̒P�ꂪ���邱�Ƃ�z��
    int q;cin >> q;
    vector<string> word(q);
    vector<vector<string>> ans_word(q); //�܂Ƃ߂ďo��
    for(int i=0;i<q;i++){
        cin >> word[i];
    }
    for(int i=0;i<q;i++){
        sort(word[i].begin(),word[i].end()); //������̃\�[�g

        //�񕪒T�� �����ɓ����ĂȂ��������0���o��
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

    //�o��
    for(size_t i=0;i<q;i++){
        for(size_t j=0;j<ans_word[i].size();j++){
            cout << ans_word[i][j] << " ";
        }
        cout << "\n";
    }
}

//�e�X�g��{6 a aa ab comprehensibility 1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}
//�󕶎���̏ꍇ�͒P�ꐔ�ɃJ�E���g����Ȃ�