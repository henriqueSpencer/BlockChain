import hashlib, json, copy
from time import time
import bitcoinlib
#sudo apt-get install libssl-dev
#sudo apt-get  = brew

DIFFICULTY = 4  # Quantidade de zeros (em hex) iniciais no hash considerado válido (resposta ao puzzle criptográfico no proof-of-work).

class Blockchain(object):
    '''Classe utilizada para representar um blockchain privado baseado no protocolo Bitcoin.'''

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        '''Cria, minera e retorna o bloco gênesis do blockchain. Chamado somente no construtor.'''
        genesis_block = self.createBlock()
        self.mineProofOfWork(self.prevBlock)
        return genesis_block

    def createBlock(self):
        '''Cria um novo bloco, inclui todas as transações pendentes e adiciona ao chain. O bloco ainda não tem nonce válido.'''
        block = {
            'index': len(self.chain),
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': '0'*64,
            'nonce': 0,
            'previousHash': self.getBlockID(self.chain[-1]) if (len(self.chain)) else '0'*64
        }
        self.memPool = []
        self.chain.append(block)
        return block

    def mineProofOfWork(self, block):
        '''Retorna um nonce válido para o bloco passado como argumento.'''
        # TODO Implemente seu código aqui.
        nonce=-1
        valido = False
        #while hash_gerado.startswith('0000') != True:
        while valido != True:
            nonce += 1
            valido = self.isValidProof(block, nonce)

        return nonce

    @staticmethod
    def isValidProof(block, nonce):
        '''Retorna `True` caso o nonce passado como argumento seja válido para o block passado como argumento, `False` caso contrário.'''
        # TODO Implemente seu código aqui.
        block['nonce'] = nonce
        hash_gerado = Blockchain.getBlockID(block)
        comeca = DIFFICULTY*'0'
        if hash_gerado.startswith(comeca) == True:
            return True
        else:
            return False

    @staticmethod
    def generateHash(data):
        '''Retorna a hash SHA256 dos dados passados como argumento.'''
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        '''Retorna o ID do bloco passado como argumento. O ID de um bloco é o hash do seu cabeçalho.'''
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

    def printChain(self):
        # Mantenha seu método de impressão do blockchain feito nas práticas passadas.
        return self.chain

    @property
    def prevBlock(self):
        '''Retorna o último bloco da chain.'''
        return self.chain[-1]

    @staticmethod
    def getWifCompressedPrivateKey(private_key=None):
        '''Retorna a chave privada no formato WIF-compressed da chave privada hex.'''
        if private_key is None:
            private_key = bitcoinlib.random_key()
        return bitcoinlib.encode_privkey(bitcoinlib.decode_privkey((private_key + '01'), 'hex'), 'wif')

    @staticmethod
    def getBitcoinAddressFromWifCompressed(wif_pkey):
        '''Retorna o endereço Bitcoin da chave privada WIF-compressed.'''
        return bitcoinlib.pubkey_to_address(bitcoinlib.privkey_to_pubkey(wif_pkey))

    @staticmethod
    def sign(wifCompressedPrivKey, message):
        '''Retorna a assinatura digital da mensagem e a respectiva chave privada WIF-compressed.'''
        return bitcoinlib.ecdsa_sign(message, wifCompressedPrivKey)

    @staticmethod
    def verifySignature(address, signature, message):
        '''Verifica se a assinatura é correspondente a mensagem e o endereço BTC.
                Você pode verificar aqui também: https://www.bitcoin.com/tools/verify-message/'''
        return bitcoinlib.ecdsa_verify(message, signature, address)


if __name__ == '__main__':
    # Todo: Teste 01
    addr = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF'
    privKey = 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U'
    message = 'Bora assinar essa mensagem?'

    signature = Blockchain.sign(privKey, message)

    print('Mensagem: {}'.format(message))
    print('Endereço BTC: {}'.format(addr))
    print('Assinatura gerada: {}'.format(signature))
    print('Assinatura válida para mensagem e endereço indicado? {}'.format(
        Blockchain.verifySignature(addr, signature, message)))


    # Todo: Teste 00
    #incrementar nonce e validar se resolveu
    # blockchain = Blockchain()
    # for x in range(0, 4):
    #     blockchain.createBlock()
    #     blockchain.mineProofOfWork(blockchain.prevBlock)
    #
    # result_1_true = Blockchain.isValidProof({'index': 1, 'timestamp': 1637007513, 'transactions': [], 'merkleRoot': '0000000000000000000000000000000000000000000000000000000000000000', 'nonce': 0, 'previousHash': '000067f74e13a541df3233b89d46c917834a41e5ac75bb4b2aeed019a075f2ab'}, 102208)
    #
    # result_1_false = Blockchain.isValidProof({'index': 1, 'timestamp': 1637007513, 'transactions': [], 'merkleRoot': '0000000000000000000000000000000000000000000000000000000000000000', 'nonce': 0, 'previousHash': '000067f74e13a541df3233b89d46c917834a41e5ac75bb4b2aeed019a075f2ab'}, 102207)
    #
    # result_2_true = Blockchain.isValidProof({'index': 4, 'timestamp': 1637007516, 'transactions': [], 'merkleRoot': '0000000000000000000000000000000000000000000000000000000000000000', 'nonce': 50650, 'previousHash': '0000f70ea3170594c1a853e7b9e1d7978301177185c6bbf5994747152ac1bc6a'}, 50650)
    #
    # result_2_false = Blockchain.isValidProof({'index': 4, 'timestamp': 1637007516, 'transactions': [], 'merkleRoot': '0000000000000000000000000000000000000000000000000000000000000000', 'nonce': 50650, 'previousHash': '0000f70ea3170594c1a853e7b9e1d7978301177185c6bbf5994747152ac1bc6a'}, 50651)
    #
    # print('fim')
    #
    #
    # block = {'index': 7, 'timestamp': 1637008057, 'transactions': [], 'merkleRoot': '0000000000000000000000000000000000000000000000000000000000000000', 'nonce': 0, 'previousHash': '00009aae5ad52e746ae7e7c5b58bbc4062eda59d3088b0a573899831280e2753'}
    #
    # blockchain = Blockchain()
    #
    # nonce = blockchain.mineProofOfWork(block)