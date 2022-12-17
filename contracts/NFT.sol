//SPDX-License-Identifier: MIT
//Contract based on [https://docs.openzeppelin.com/contracts/3.x/erc721](https://docs.openzeppelin.com/contracts/3.x/erc721)

pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/utils/Counters.sol";


contract NFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    using Strings for uint256;

    Counters.Counter private tokenCounter;

    string private baseURI;
   

   
    uint256 constant public MAX_SUPPLY = 30;
    uint8 constant public MAX_NFT_PER_WALLET = 1;
    // bool public isSaleActive;

   
    bytes32 public merkleRoot;

   
    mapping(address => bool) public granted;

    // ============ ACCESS CONTROL/SANITY MODIFIERS ============


    modifier isValidMerkleProof(bytes32[] calldata merkleProof, bytes32 root, uint256 index, address to ) {
      require(
            MerkleProof.verify(
                merkleProof,
                root,
                keccak256(abi.encodePacked(index, to))
            ),
            "Address does not exist in list"
        );
        _;
        
    }

    modifier maxNFTPerWallet(uint256 numberOfTokens) {
        require(
            balanceOf(msg.sender) + numberOfTokens <= MAX_NFT_PER_WALLET,
            "Max witches to mint is three"
        );
        _;
    }


    constructor(
     string memory _name,
     string memory _symbol, 
     bytes32 _merkleRoot
    ) ERC721(_name, _symbol) {
     
       merkleRoot = _merkleRoot;
    }

    // ============ PUBLIC FUNCTIONS FOR MINTING ============

    function grantNFT(
        uint8 numberOfTokens,
        bytes32[] calldata merkleProof,
        uint256 index,
        address to
        
    )
        onlyOwner
        external
        isValidMerkleProof(merkleProof, merkleRoot, index, to)
       
    {
        

        require(
            tokenCounter.current() + numberOfTokens <= MAX_SUPPLY,
            "Not enough witches remaining to mint"
        );

        require(!granted[to], "Already granted nft");
        

        for (uint256 i = 0; i < numberOfTokens; i++) {
            _safeMint(to, nextTokenId());
        }
    }



    // ============ PUBLIC READ-ONLY FUNCTIONS ============

    function getBaseURI() external view returns (string memory) {
        return baseURI;
    }


    // ============ OWNER-ONLY ADMIN FUNCTIONS ============

   
     function setTokenURI(string memory _tokenURI) external  onlyOwner {
        baseURI = _tokenURI;
    } 

    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }

    function withdrawTokens(IERC20 token) public onlyOwner {
        uint256 balance = token.balanceOf(address(this));
        token.transfer(msg.sender, balance);
    }


    /**
     * @dev See {IERC721Metadata-tokenURI}.
     */
    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(_exists(tokenId), "Nonexistent token");

        return baseURI;
           
    }

    function nextTokenId() private returns (uint256) {
        tokenCounter.increment();
        return tokenCounter.current();
    }


}



