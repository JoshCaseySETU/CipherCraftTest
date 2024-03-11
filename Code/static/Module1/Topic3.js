// Define functions for Vigenère cipher encryption and decryption
function encryptVigenere(message, key) {
    // Convert the message and key to uppercase for simplicity
    message = message.toUpperCase();
    key = key.toUpperCase();
    
    // Initialize an empty string to store the encrypted message
    let encryptedMessage = '';
    
    // Initialize a variable to keep track of the position in the key
    let keyIndex = 0;
    
    // Iterate through each character in the message
    for (let i = 0; i < message.length; i++) {
        const char = message[i];
        
        // Check if the character is a letter
        if (char.match(/[A-Z]/)) {
            // Get the ASCII code of the character
            let charCode = message.charCodeAt(i);
            
            // Get the ASCII code of the corresponding key character
            let keyCode = key.charCodeAt(keyIndex % key.length);
            
            // Apply the Vigenère cipher encryption formula
            charCode = ((charCode - 65 + keyCode - 65) % 26) + 65;
            
            // Increment the key index
            keyIndex++;
            
            // Convert the ASCII code back to a character and append to the encrypted message
            encryptedMessage += String.fromCharCode(charCode);
        } else {
            // If the character is not a letter, keep it unchanged
            encryptedMessage += char;
        }
    }
    
    // Return the encrypted message
    return encryptedMessage;
}

function decryptVigenere(encryptedMessage, key) {
    // Convert the key to uppercase for simplicity
    key = key.toUpperCase();
    
    // Initialize an empty string to store the decrypted message
    let decryptedMessage = '';
    
    // Initialize a variable to keep track of the position in the key
    let keyIndex = 0;
    
    // Iterate through each character in the encrypted message
    for (let i = 0; i < encryptedMessage.length; i++) {
        const char = encryptedMessage[i];
        
        // Check if the character is a letter
        if (char.match(/[A-Z]/)) {
            // Get the ASCII code of the character
            let charCode = encryptedMessage.charCodeAt(i);
            
            // Get the ASCII code of the corresponding key character
            let keyCode = key.charCodeAt(keyIndex % key.length);
            
            // Apply the Vigenère cipher decryption formula
            charCode = ((charCode - 65 - (keyCode - 65) + 26) % 26) + 65;
            
            // Increment the key index
            keyIndex++;
            
            // Convert the ASCII code back to a character and append to the decrypted message
            decryptedMessage += String.fromCharCode(charCode);
        } else {
            // If the character is not a letter, keep it unchanged
            decryptedMessage += char;
        }
    }
    
    // Return the decrypted message
    return decryptedMessage;
}


