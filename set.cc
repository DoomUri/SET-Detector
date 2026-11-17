#include <iostream>
#include <vector>

using namespace std;

struct Carta{
    string color, textura, forma;
    int numero;
};

int main(){
    /*
    cout << "Hola!! Est" << char(133) << "s executant el detector de sets." << endl << endl;
    cout << "Per tal de comen" << char(135) << "ar introdueix totes les cartes que vols tenir" << endl;
    cout << "en compte separades per un espai i amb un 0 al final. Seguint el format seg" << char(129) << "ent:" << endl << endl;
    cout << "color1,textura1,forma1,quantitat1 color2,textura2,forma2,quantitat2 (...) 0" << endl << endl; 
    cout << "On:" << endl;
    cout << "- color pot ser: vermell / lila / verd." << endl;
    cout << "- textura pot ser: opac / buit / ratllat." << endl;
    cout << "- forma pot ser: rombe / serp / oval." << endl;
    cout << "- quantitat pot ser: 1 / 2 / 3." << endl << endl;
    cout << "Assegura't d'escriure-ho tot correctament i no deixar-te comes o espais." << endl << endl;
    cout << "Per a posar un exemple, una possible entrada de 3 cartes seria:" << endl;
    cout << "vermell,opac,rombe,1 lila,opac,oval,2 verd,opac,serp,3 0" << endl << endl;
    */
    //while(0 == 0){
        //cout << "Escriu aqu" << char(161) << " les teves cartes: ";
        char a;
        vector <Carta> llista;
        cin >> a;
        while(a != '0'){
            Carta res;
            while(a != ','){
                res.color.push_back(a);
                cin >> a;
            }
            cin >> a;
            while(a != ','){
                res.textura.push_back(a);
                cin >> a;
            }
            cin >> a;
            while(a != ','){
                res.forma.push_back(a);
                cin >> a;
            }
            cin >> res.numero;
            llista.push_back(res);
            cin >> a;
        }

        int count = 0;
        //cout << endl;
        if(llista.size() > 2) for(int i = 0; i < llista.size()-2; ++i) for(int j = i+1; j < llista.size()-1; ++j) for(int k = j+1; k < llista.size(); ++k){
            bool set = true;
            if(not(llista[i].color == llista[j].color and llista[j].color == llista[k].color) and 
            not(llista[i].color != llista[j].color and llista[j].color != llista[k].color and llista[i].color != llista[k].color)) set = false;

            if(set and not(llista[i].textura == llista[j].textura and llista[j].textura == llista[k].textura) and 
            not(llista[i].textura != llista[j].textura and llista[j].textura != llista[k].textura and llista[i].textura != llista[k].textura)) set = false;

            if(set and not(llista[i].forma == llista[j].forma and llista[j].forma == llista[k].forma) and 
            not(llista[i].forma != llista[j].forma and llista[j].forma != llista[k].forma and llista[i].forma != llista[k].forma)) set = false;

            if(set and not(llista[i].numero == llista[j].numero and llista[j].numero == llista[k].numero) and 
            not(llista[i].numero != llista[j].numero and llista[j].numero != llista[k].numero and llista[i].numero != llista[k].numero)) set = false;

            if(set){
                ++ count;
                cout << i+1 << " " << j+1 << " " << k+1 << " ";
                //cout << "Set " << count << ": " << "Cartes " << i+1 << ", " << j+1 << ", " << k+1 << "." << endl;
            }
        }
        //if(count == 0) cout << "No hi ha cap Set." << endl;
        //cout << endl;        
    //}
}