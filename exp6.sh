sudo apt-get install gnupg -y
gpg --version

cat > alice_key_params <<EOF
%no-protection
Key-Type: RSA
Key-Length: 2048
Name-Real: Alice Example
Name-Email: alice@example.com
Expire-Date: 0
%commit
EOF
gpg --batch --generate-key alice_key_params

cat > bob_key_params <<EOF
%no-protection
Key-Type: RSA
Key-Length: 2048
Name-Real: Bob Example
Name-Email: bob@example.com
Expire-Date: 0
%commit
EOF
gpg --batch --generate-key bob_key_params

gpg --armor --export alice@example.com > alice_pub.asc
gpg --armor --export bob@example.com > bob_pub.asc
gpg --import alice_pub.asc
gpg --import bob_pub.asc

echo "Hi Alice, this is a secret message" > message.txt
gpg --encrypt --recipient alice@example.com --armor -o message_to_alice.asc message.txt

gpg --output decrypted.txt --decrypt message_to_alice.asc
cat decrypted.txt

echo "Report content" > report.pdf
cp report.pdf report_original.pdf
gpg --output report.sig --detach-sign report.pdf
gpg --verify report.sig report.pdf

echo "tampered!" >> report.pdf
gpg --verify report.sig report.pdf

sudo apt-get update -y
sudo apt-get install expect -y

cat > charlie_key_params <<EOF
%no-protection
Key-Type: RSA
Key-Length: 2048
Name-Real: Charlie Example
Name-Email: charlie@example.com
Expire-Date: 0
%commit
EOF
gpg --batch --generate-key charlie_key_params

gpg --output charlie_revocation.asc --gen-revoke charlie@example.com <<EOF
y
0
Revoking key
y
EOF
