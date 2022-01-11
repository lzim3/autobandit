from pwn import *
import banditcommands


class AutoBandit:

    def __init__(self, level, level_password):
        self.level = level
        self.level_password = level_password
        self.establish_connection()
        self.solutions = banditcommands.solutions

    def establish_connection(self):
        self.session = ssh('bandit%d' % self.level, 'bandit.labs.overthewire.org', password=self.level_password, port=2220)
        self.io = self.session.process('bash')
        time.sleep(1)
        print()
        print('Level %d Access Granted!' % (self.level))
        time.sleep(1)

    def execute_bash_command(self, list_command):
        for command in list_command:
            print('Sending %s to the terminal' % (command.decode('utf-8')), end='')
            self.io.sendline(command)
            self.io.recv()
            time.sleep(0.6)
            print('.', end='')
            time.sleep(0.6)
            print('.', end='')
            time.sleep(0.6)
            print('.', end='')
            time.sleep(1)

    def receive_password(self):
        self.level_password = self.io.recvline().decode('utf-8').strip()
        print('\nBingo! The password for this level is %s. Let\'s go to the next level!' % (self.level_password))
        self.level += 1
        time.sleep(2)

    def level_0_to_10(self):
        for list_command in self.solutions.values():
            self.execute_bash_command(list_command)
            self.receive_password()
            self.establish_connection()
        print()
        print('Complete. Goodbye...')


if __name__ == "__main__":
    automateProcess = AutoBandit(0, 'bandit0')
    automateProcess.level_0_to_10()