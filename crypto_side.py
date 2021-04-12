import rsa
from Crypto.Hash import SHA256
from logger import Logger
import os
import secrets

'''
This module emplements abstract class 'CryptoSide'
of participant of 'handshake' protocol, 
which can transfer 'command'

'b_side'-like are acronims from Bob-side -
second participant of 'handshake' protocol
'''

# class implements Exception of 'handshake'
class VerifyError(Exception):
    discription = 'signature not verified'

'''
This class encapsulates 'challenge',
because rsa library need it to have
'read' method
'''

class ChallengeMsg:
    content = ''

    def __init__(self, p_num):
        self.content = str(p_num).encode()

    def read(self, x):
        return self.content

    def get_text(self):
        return self.content


class CryptoSide:
    name = '' # name of participant
    (__secret_key, public_key) = rsa.newkeys(1024)
    b_key = '' # key of second (Bob) side
    command = '' # command that is selected on trinket and must be execute on car
    inner_challenge = '' # cache of sended to Bob challenge
    outer_challenge = '' # cache of recived from Bob challenge
    signature = '' # confirmation of recived from Bob challenge

    def __init__(self, p_name):
        self.name = p_name

    def get_pubkey(self):
        return self.public_key



    def reset_keys(self):
        (self.public_key, self.__secret_key) = rsa.newkeys(512)
        Logger.log('{} keys reset'.format(self.name))

    def set_side_pubkey(self, p_side_b):
        self.b_key = p_side_b.get_pubkey()



    '''
    emulates selecting command manually
    p_cmd = 0 - open
            1 - close
            other - unknown
    '''
    def set_command(self, p_cmd):
        Logger.log('{} command set: {}'.format(self.name, p_cmd))
        self.command = p_cmd

    def get_command(self):
        return self.command

    def generate_challenge(self):
        chg = secrets.token_hex(nbytes=256)

        # challenge need to be transformed from objects to strings/bytes/nums
        self.inner_challenge = ChallengeMsg(SHA256
            .new(chg.encode())
            .hexdigest())

        Logger.log('{} challenge generated'.format(self.name))
        return self.inner_challenge



    def set_outer_challenge(self, p_side_b):
        self.outer_challenge = p_side_b.generate_challenge()
        Logger.log('{} got challenge'.format(self.name))

    def check_confirmation(self, p_side_b):
        Logger.log('{} prepare to sign...'.format(p_side_b.name))
        b_sign = p_side_b.sign()
        Logger.log('{} checking sign...'.format(self.name))
        try:
            rsa.verify(self.inner_challenge, b_sign, self.b_key)
        except: 
            raise VerifyError('unverified signature')


    '''
    method signs 'challenge', 
    if challenge is empty (expired),
        it throws Exception
    '''
    def sign(self):
        try:
            self.signature = rsa.sign(self.outer_challenge, self.__secret_key, 'SHA-1')
        except: 
            raise VerifyError('double use of command')
        Logger.log('{} signed'.format(self.name))
        return self.signature


    '''
    function expires challenges,
    when command is executed to
    keep protocol safe from re-use
    of command
    '''
    def expire_challenges(self):
        self.inner_challenge = ''
        self.outer_challenge = ''
        Logger.log('{} challenges expired'.format(self.name))