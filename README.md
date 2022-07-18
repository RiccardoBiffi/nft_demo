SimpleCollectible:
- mint an NFT using IPFS data already deployed by somebody else
- anybody can mint multiple NFT, all with the same properties.

AdvancedCollectible:
- mint NFT using chainlink VRF to randomly choose the dog breed (and so the image).
- NFT metadata is created and deployed to IPFS throught a local node, creating the image URI
- if the local node goes down and nobody synched my files, they are unreachable. Pinata solve this. I can upload to this service based on IPFS, it still returns the image URI
- after uploading the image and the metadata to ipfs, I can set the token URI of the NFTs to the uploaded metadata