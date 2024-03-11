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
