// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./ERC721A.sol";



contract RewardNFT is Ownable, ERC721A {

    string private _baseTokenURI;

    constructor() ERC721A("You", "YO") {

    }

    function mint(address to, uint256 quantity) external onlyOwner {
        _mint(to, quantity);
    }

    function setBaseURI(string calldata baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }

    function _baseURI() internal view override returns(string memory) {
        return _baseTokenURI;
    }

     function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        return _baseTokenURI;
    }
}