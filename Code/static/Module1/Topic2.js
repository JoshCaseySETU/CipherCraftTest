// Define functions for Caesar cipher encryption and decryption
function encryptCaesar(message, shiftAmount) {
    // Convert the message to uppercase for simplicity
    message = message.toUpperCase();
    
    // Initialize an empty string to store the encrypted message
    let encryptedMessage = '';
    
    // Iterate through each character in the message
    for (let i = 0; i < message.length; i++) {
        const char = message[i];
        
        // Check if the character is a letter
        if (char.match(/[A-Z]/)) {
            // Get the ASCII code of the character
            let charCode = message.charCodeAt(i);
            
            // Apply the shift to the ASCII code
            charCode = ((charCode - 65 + shiftAmount) % 26) + 65;
            
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

function decryptCaesar(encryptedMessage, shiftAmount) {
    // Decrypting a Caesar cipher is essentially encrypting with a negative shift
    return encryptCaesar(encryptedMessage, -shiftAmount);
}

// Define function for frequency analysis
function frequencyAnalysis(encryptedMessage) {
    // Convert the message to uppercase for simplicity
    encryptedMessage = encryptedMessage.toUpperCase();
    
    // Initialize an object to store the frequency of each letter
    const frequency = {};
    
    // Iterate through each character in the message
    for (let i = 0; i < encryptedMessage.length; i++) {
        const char = encryptedMessage[i];
        
        // Check if the character is a letter
        if (char.match(/[A-Z]/)) {
            // Increment the count for this letter in the frequency object
            frequency[char] = (frequency[char] || 0) + 1;
        }
    }
    
    // Return the frequency object
    return frequency;
}



