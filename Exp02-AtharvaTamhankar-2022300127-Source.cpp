#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <map>

using namespace std;

class TranspositionCiphers
{
private:
    // Helper function to remove spaces and convert to uppercase
    string preprocessText(string text)
    {
        string result = "";
        for (char c : text)
        {
            if (isalpha(c))
            {
                result += toupper(c);
            }
        }
        return result;
    }

public:
    // Rail Fence Cipher Implementation
    string railFenceEncrypt(string plaintext, int rails)
    {
        if (rails == 1)
            return plaintext;

        plaintext = preprocessText(plaintext);
        vector<string> fence(rails);
        int rail = 0;
        bool down = false;

        // Create the rail fence pattern
        for (int i = 0; i < plaintext.length(); i++)
        {
            fence[rail] += plaintext[i];

            if (rail == 0 || rail == rails - 1)
            {
                down = !down;
            }

            rail += down ? 1 : -1;
        }

        // Read off the rails
        string ciphertext = "";
        for (int i = 0; i < rails; i++)
        {
            ciphertext += fence[i];
        }

        return ciphertext;
    }

    string railFenceDecrypt(string ciphertext, int rails)
    {
        if (rails == 1)
            return ciphertext;

        vector<string> fence(rails);
        vector<int> railLens(rails, 0);
        int rail = 0;
        bool down = false;

        // Calculate length of each rail
        for (int i = 0; i < ciphertext.length(); i++)
        {
            railLens[rail]++;

            if (rail == 0 || rail == rails - 1)
            {
                down = !down;
            }

            rail += down ? 1 : -1;
        }

        // Fill the rails with ciphertext
        int index = 0;
        for (int i = 0; i < rails; i++)
        {
            fence[i] = ciphertext.substr(index, railLens[i]);
            index += railLens[i];
        }

        // Read off in zigzag pattern
        string plaintext = "";
        rail = 0;
        down = false;
        vector<int> railIndex(rails, 0);

        for (int i = 0; i < ciphertext.length(); i++)
        {
            plaintext += fence[rail][railIndex[rail]++];

            if (rail == 0 || rail == rails - 1)
            {
                down = !down;
            }

            rail += down ? 1 : -1;
        }

        return plaintext;
    }

    // Columnar Transposition Cipher Implementation
    string columnarTranspositionEncrypt(string plaintext, string key)
    {
        plaintext = preprocessText(plaintext);
        key = preprocessText(key);

        int keyLen = key.length();
        int rows = (plaintext.length() + keyLen - 1) / keyLen;

        // Create matrix
        vector<vector<char>> matrix(rows, vector<char>(keyLen, 'X'));

        // Fill matrix with plaintext
        int index = 0;
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < keyLen && index < plaintext.length(); j++)
            {
                matrix[i][j] = plaintext[index++];
            }
        }

        // Create key order
        vector<pair<char, int>> keyOrder;
        for (int i = 0; i < keyLen; i++)
        {
            keyOrder.push_back({key[i], i});
        }
        sort(keyOrder.begin(), keyOrder.end());

        // Read columns in key order
        string ciphertext = "";
        for (int k = 0; k < keyLen; k++)
        {
            int col = keyOrder[k].second;
            for (int i = 0; i < rows; i++)
            {
                ciphertext += matrix[i][col];
            }
        }

        return ciphertext;
    }

    string columnarTranspositionDecrypt(string ciphertext, string key)
    {
        key = preprocessText(key);

        int keyLen = key.length();
        int rows = ciphertext.length() / keyLen;

        // Create key order
        vector<pair<char, int>> keyOrder;
        for (int i = 0; i < keyLen; i++)
        {
            keyOrder.push_back({key[i], i});
        }
        sort(keyOrder.begin(), keyOrder.end());

        // Create matrix and fill with ciphertext
        vector<vector<char>> matrix(rows, vector<char>(keyLen));
        int index = 0;

        for (int k = 0; k < keyLen; k++)
        {
            int col = keyOrder[k].second;
            for (int i = 0; i < rows; i++)
            {
                matrix[i][col] = ciphertext[index++];
            }
        }

        // Read row by row
        string plaintext = "";
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < keyLen; j++)
            {
                if (matrix[i][j] != 'X')
                {
                    plaintext += matrix[i][j];
                }
            }
        }

        return plaintext;
    }

    // Double Transposition Cipher Implementation
    string doubleTranspositionEncrypt(string plaintext, string key1, string key2)
    {
        // First transposition
        string intermediate = columnarTranspositionEncrypt(plaintext, key1);
        // Second transposition
        string ciphertext = columnarTranspositionEncrypt(intermediate, key2);
        return ciphertext;
    }

    string doubleTranspositionDecrypt(string ciphertext, string key1, string key2)
    {
        // Reverse the process: decrypt with key2 first, then key1
        string intermediate = columnarTranspositionDecrypt(ciphertext, key2);
        string plaintext = columnarTranspositionDecrypt(intermediate, key1);
        return plaintext;
    }

    // Menu-driven interface
    void runMenu()
    {
        int choice;
        string plaintext, ciphertext, key, key1, key2;
        int rails;

        while (true)
        {
            cout << "\n=== TRANSPOSITION CIPHER MENU ===" << endl;
            cout << "1. Rail Fence Cipher" << endl;
            cout << "2. Columnar Transposition Cipher" << endl;
            cout << "3. Double Transposition Cipher" << endl;
            cout << "4. Quit" << endl;
            cout << "Enter your choice (1-4): ";
            cin >> choice;
            cin.ignore(); // Clear the newline character

            switch (choice)
            {
            case 1:
            {
                cout << "\n--- RAIL FENCE CIPHER ---" << endl;
                cout << "Enter plaintext: ";
                getline(cin, plaintext);
                cout << "Enter number of rails: ";
                cin >> rails;
                cin.ignore();

                ciphertext = railFenceEncrypt(plaintext, rails);
                cout << "Encrypted text: " << ciphertext << endl;

                string decrypted1 = railFenceDecrypt(ciphertext, rails);
                cout << "Decrypted text: " << decrypted1 << endl;
                break;
            }

            case 2:
            {
                cout << "\n--- COLUMNAR TRANSPOSITION CIPHER ---" << endl;
                cout << "Enter plaintext: ";
                getline(cin, plaintext);
                cout << "Enter key: ";
                getline(cin, key);

                ciphertext = columnarTranspositionEncrypt(plaintext, key);
                cout << "Encrypted text: " << ciphertext << endl;

                string decrypted2 = columnarTranspositionDecrypt(ciphertext, key);
                cout << "Decrypted text: " << decrypted2 << endl;
                break;
            }

            case 3:
            {
                cout << "\n--- DOUBLE TRANSPOSITION CIPHER ---" << endl;
                cout << "Enter plaintext: ";
                getline(cin, plaintext);
                cout << "Enter first key: ";
                getline(cin, key1);
                cout << "Enter second key: ";
                getline(cin, key2);

                ciphertext = doubleTranspositionEncrypt(plaintext, key1, key2);
                cout << "Encrypted text: " << ciphertext << endl;

                string decrypted3 = doubleTranspositionDecrypt(ciphertext, key1, key2);
                cout << "Decrypted text: " << decrypted3 << endl;
                break;
            }

            case 4:
                cout << "Exiting program. Goodbye!" << endl;
                return;

            default:
                cout << "Invalid choice! Please enter 1-4." << endl;
                break;
            }
        }
    }
};

int main()
{
    TranspositionCiphers cipher;

    cout << "Welcome to Transposition Ciphers Implementation!" << endl;
    cout << "This program implements Rail Fence, Columnar Transposition, and Double Transposition ciphers." << endl;

    cipher.runMenu();

    return 0;
}