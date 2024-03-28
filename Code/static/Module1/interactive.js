function encryptHieroglyphic(message) {
    // Create a mapping of characters to hieroglyphic symbols
    const hieroglyphicMapping = {
        'A': '𓃀',
        'B': '𓂋',
        'C': '𓅱',
        'D': '𓀀',
        'E': '𓀭',
        'F': '𓀾',
        'G': '𓁹',
        'H': '𓆱',
        'I': '𓍯',
        'J': '𓃾',
        'K': '𓆛',
        'L': '𓂧',
        'M': '𓇌',
        'N': '𓆑',
        'O': '𓁨',
        'P': '𓈖',
        'Q': '𓄿',
        'R': '𓅓',
        'S': '𓂋',
        'T': '𓏏',
        'U': '𓃭',
        'V': '𓀓',
        'W': '𓀭𓁷',
        'X': '𓏭',
        'Y': '𓀠',
        'Z': '𓆱',
        ' ': ' ',
    };

    // Convert the message to uppercase for simplicity
    message = message.toUpperCase();

    // Initialize an empty string to store the encrypted message
    let encryptedMessage = '';

    // Iterate through each character in the message
    for (let i = 0; i < message.length; i++) {
        const char = message[i];
        
        // Check if the character exists in the mapping
        if (hieroglyphicMapping.hasOwnProperty(char)) {
            // If yes, append the corresponding hieroglyphic symbol to the encrypted message
            encryptedMessage += hieroglyphicMapping[char];
        } else {
            // If not, keep the character unchanged
            encryptedMessage += char;
        }
    }

    // Return the encrypted message
    return encryptedMessage;
}


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

function encryptFence(message, numRails) {
    let rail = new Array(numRails).fill().map(() => new Array(message.length).fill('\n'));
    let dir_down = false;
    let row = 0, col = 0;
   
    for (let i = 0; i < message.length; i++) {
      if (row == 0 || row == numRails - 1) dir_down = !dir_down;
      rail[row][col++] = message[i];
      dir_down ? row++ : row--;
    }
   
    let result = '';
    for (let i = 0; i < numRails; i++)
      for (let j = 0; j < message.length; j++)
        if (rail[i][j] != '\n') result += rail[i][j];
   
    return result;
}

function decryptFence(encryptedMessage, numRails) {
    let rail = new Array(numRails).fill().map(() => new Array(encryptedMessage.length).fill('\n'));
    let dir_down = false;
    let row = 0, col = 0;
   
    for (let i = 0; i < encryptedMessage.length; i++) {
      if (row == 0) dir_down = true;
      if (row == numRails - 1) dir_down = false;
      rail[row][col++] = '*';
      dir_down ? row++ : row--;
    }
   
    let index = 0;
    for (let i = 0; i < numRails; i++)
      for (let j = 0; j < encryptedMessage.length; j++)
        if (rail[i][j] == '*' && index < encryptedMessage.length) rail[i][j] = encryptedMessage[index++];
   
    let result = '';
    row = 0, col = 0;
    for (let i = 0; i < encryptedMessage.length; i++) {
      if (row == 0) dir_down = true;
      if (row == numRails - 1) dir_down = false;
      if (rail[row][col] != '*') result += rail[row][col++];
      dir_down ? row++ : row--;
    }
   
    return result;
}



