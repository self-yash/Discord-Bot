Bank Management System using Discord Bot
# Discord Bank Bot

A feature-rich Discord bot built with Python to simulate a bank system using Firebase Firestore as the backend database. The bot allows users to register, login, deposit money, withdraw money, check account balances, and close accounts.

## Features

- **User Registration**: Register new users with a username, date of birth, and branch.
- **User Login**: Secure login using a 4-digit numeric password.
- **Balance Management**:
  - Deposit money
  - Withdraw money (with balance checks)
  - View balance
- **Account Closing**: Close an account after withdrawing all funds.
- **Firebase Integration**: User data is stored and retrieved securely using Firebase Firestore.
- **Interactive Commands**: Powered by Discord's command framework, making it easy to interact with the bot.

## Commands

### `!register <username> <password> <date_of_birth> <branch>`
Register a new user.
- **Example**:
  ```
  !register JohnDoe 1234 2000-01-01 NewYork
  ```

### `!login <username> <password>`
Login as a registered user.
- **Example**:
  ```
  !login JohnDoe 1234
  ```

### Interactive Commands After Login:
- **Withdraw Money**
- **Deposit Money**
- **Check Balance**
- **Close Account**
- **Logout**

## Firebase Structure
The bot uses the following Firestore structure:
- **Collection**: `users`
  - **Document**: `{username}`
    - `FullName`: Full name of the user
    - `DoB`: Date of Birth
    - `Branch`: Branch name
    - `Balance`: Current account balance
    - `password`: 4-digit numeric password

## Error Handling
- Invalid inputs and timeouts are handled gracefully.
- Users are guided with prompts for required actions.

## Future Enhancements
- Add analytics to track usage trends.
- Expand financial services and integrate with external APIs.
- Improve user experience with detailed error messages and custom embeds.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Discord.py](https://discordpy.readthedocs.io/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/)
