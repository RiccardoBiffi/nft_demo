// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBaseV2 {
    uint256 public tokenCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    struct Dog {
        Breed breed;
        uint256 base;
        uint256 descr_exclamation;
        uint256 cuteness;
        uint256 bark_power;
    }

    mapping(uint256 => Dog) public tokenId_Dog;
    mapping(uint256 => address) public requestId_Sender;

    // Best practice: create an event for every mapping update
    //   Events are logs on the blockchain, not accessible to smart contracts
    //   The backend caller can read them on the transaction receipt
    //   Useful for testing and debugging

    event RequestedCollectible(uint256 indexed requestId, address from);
    event AttributesAssigned(uint256 indexed tokenId, Dog breed);
    event RequestedRandomness(uint256 requestId);
    event FullfillRandomWordsCalled();

    // Chainlink VRF properties
    // Request
    VRFCoordinatorV2Interface COORDINATOR;
    uint64 subscriptionId; // my subId to the chainlink service
    address vrfCoordinator;
    address link;
    bytes32 keyHash; // gas lane
    uint32 callbackGasLimit; // About 20k WEI / random-word
    uint16 requestConfirmations; // Block confirmations before callback
    uint32 numWords; // Random words to generate

    // Response
    uint256 public randomWord;
    uint256 public requestId;

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        uint64 _subscriptionId,
        bytes32 _keyhash,
        uint32 _callbackGasLimit,
        uint16 _requestConfirmations,
        uint32 _numWords
    ) VRFConsumerBaseV2(_vrfCoordinator) ERC721("Dogie", "DOG") {
        tokenCounter = 0;
        vrfCoordinator = _vrfCoordinator;
        link = _linkToken;
        subscriptionId = _subscriptionId;
        keyHash = _keyhash;
        callbackGasLimit = _callbackGasLimit;
        requestConfirmations = _requestConfirmations;
        numWords = _numWords;

        COORDINATOR = VRFCoordinatorV2Interface(vrfCoordinator);
    }

    function createCollectible() public returns (bytes32) {
        require(tokenCounter <= 9, "All Dogies have already been minted!");
        // Request a random word. I'll use it to generate the attributes of the NFT
        requestId = COORDINATOR.requestRandomWords(
            keyHash,
            subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );

        emit RequestedRandomness(requestId);

        // I save the sender so, after I got the VRN, I can mint the NFT to him
        requestId_Sender[requestId] = msg.sender;
        emit RequestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomWords(
        uint256 _requestId,
        uint256[] memory _randomWords
    ) internal override {
        randomWord = _randomWords[0];

        // Randomly obtain the attributes of this new token
        Dog memory dog = Dog(
            Breed(randomWord % 3),
            ((randomWord / 10) % 10),
            ((randomWord / 100) % 10),
            ((randomWord / 1000) % 10) + 1,
            ((randomWord / 10000) % 100) + 1
        );
        // I create a new token ID and update the counter
        uint256 newTokenId = tokenCounter;

        // I need to assign the breed to the tokenID, I'll map them
        tokenId_Dog[newTokenId] = dog;
        emit AttributesAssigned(newTokenId, dog);

        // I cannot mint with msg.sender because it's chainlink who called this method
        // Otherwise I'd assign the NFT to them! _msgSender() solve this
        address originalCaller = requestId_Sender[_requestId];
        _safeMint(originalCaller, newTokenId);
        tokenCounter++;

        //todo use _setTokenURI(newTokenId, tokenURI) here;
    }

    // Call this after fullfillRandomWords completed
    // The porpose of the function is to experiment better with IPFS
    function setTokenURI(uint256 tokenID, string memory _tokenURI) public {
        // I need to merge onchain metadata with offchain metadata
        // Onchain: 3 breeds; offchain: 3 metadata URI

        // Only the owner of the tokenID can change the tokenURI
        require(
            _isApprovedOrOwner(_msgSender(), tokenID),
            "ERC721: caller is not owner nor approved to work with this token."
        );
        _setTokenURI(tokenID, _tokenURI);
    }
}
