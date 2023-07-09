// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.4;

import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @notice Returns the two quotients and the remainder of an uneven division with a fraction. Useful for dividing ether and tokens.
/// @param dividend The dividend, which will be divided by the fraction.
/// @param numerator Numerator of fraction, which the dividend will be divided into.
/// @param denominator Denominator of fraction, which the dividend will be divided into.
function divideUnequallyIntoTwoWithRemainder(uint256 dividend, uint256 numerator, uint256 denominator) pure returns(uint256, uint256, uint256) {
    require(denominator > numerator);
    uint256 quotient1 = dividend*numerator/denominator;
    uint256 quotient2 = dividend*(denominator-numerator)/denominator;
    return (quotient1, quotient2, dividend - (quotient1 + quotient2));
}

/// @title A shardable/fractional non-fungible token that can be fractually owned via Shards.
/// @author Frederik W. L. Christoffersen
/// @notice This contract is used to fractionalize a non-fungible token. Be aware that a sell transfers a service fee of 2.5% to Counekt.
/// @dev historicShards are used to show proof of ownership at different points of time.
/// @custom:beaware This is a commercial contract.
contract Shardable {

    /// @notice A struct representing the related info of a non-fungible Shard token.
    /// @dev Is represented via a bytes32 value created from the hash: keccak256(owner, creationClock).
    /// @param amount Amount that the Shard represents.
    /// @param owner The owner of the Shard.
    /// @param creationClock The clock at which the Shard was created.
    /// @param expiredClock The clock at which the Shard expired. Default is set to the maximum value.
    struct ShardInfo {
        uint256 amount;
        address owner; 
        uint256 creationClock;        
    }

    /// @notice A struct representing the related sale info of a non-fungible Shard token.
    /// @param amount Amount that is for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to Address pointing to a potentially specifically set buyer of the sale.
    struct ShardSale {
        uint256 amount;
        address tokenAddress;
        uint256 price;
        address to;
    }

    /// @notice Integer value to implement a concept of time independently of the messy block.timestamp
    uint256 clock = 0;

    /// @notice Boolean stating if the Shardable is active and tradeable or not.
    bool public active;

    /// @notice Mapping pointing to integer value representing the total number of shards issued, provided the clock. Used as the denominator to represent a relative shard fraction.
    mapping(uint256 => uint256) public totalShardAmountByClock;

    /// @notice Mapping pointing to related info of a Shard given the bytes of a unique Shard instance.
    mapping(bytes32 => ShardInfo) public infoByShard;
    /// @notice Mapping pointing to a currently valid shard given the address of its owner.
    mapping(address => bytes32) public shardByOwner;
    /// @notice Mapping pointing to a boolean stating if a given Shard is for sale or not.
    mapping(bytes32 => bool) shardsForSale;
    /// @notice Mapping pointing to related sale info of a Shard given the bytes of a unique Shard instance.
    mapping(bytes32 => ShardSale) saleByShard;
    // @notice Mapping pointing to an expired clock given a shard.
    mapping(bytes32 => uint256) shardExpirationClock;

    /// @notice Event emitted when a Shard is created.
    /// @param shard The Shard byte identifier, which was created.
    /// @param owner The owner of the created Shard.
    /// @param creationClock The clock at which the shard was created.
    event NewShard(
        bytes32 shard,
        address owner,
        uint256 creationClock
        );

    /// @notice Event emitted when a Shard expires.
    /// @param shard The Shard byte identifier, which expired.
    /// @param expirationClock The clock at which the shard expired.
    event ExpiredShard(
        bytes32 shard,
        uint256 expirationClock
        );

    /// @notice Event emitted when a sale of a Shard is sold.
    /// @param shard The shard that was sold from.
    /// @param amount Amount of the Shard that was sold.
    /// @param to The buyer of the sale.
    /// @param tokenAddress The address of the token that was accepted in the purchase. A value of 0x0 represents ether.
    /// @param price The amount which the Shard was for sale for. The token address being the valuta.
    event SaleSold(
        bytes32 shard,
        uint256 amount,
        address to,
        address tokenAddress,
        uint256 price
        );

    /// @notice Event emitted when a Shard is put up for sale.
    /// @param shard The shard that was put for sale.
    /// @param amount Amount of the Shard put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to The specifically set buyer of the sale, if any.
    event PutForSale(
        bytes32 shard,
        uint256 amount,
        address tokenAddress,
        uint256 price,
        address to
        );

    modifier incrementClock {
        _;
        totalShardAmountByClock[clock+1] = totalShardAmountByClock[clock]; // remember the total shard amount at previous clock
        clock++;
    }
    
    /// @notice Modifier that requires the msg.sender to be a current valid Shard holder.
    modifier onlyShardHolder {
        require(isShardHolder(msg.sender), "UH");
        _;
    }

    /// @notice Modifier that requires a given Shard to be currently valid.
    modifier onlyValidShard(bytes32 shard) {
        require(isValidShard(shard), "US");
        _;
    }

    /// @notice Modifier that makes sure the entity is active and not liquidized/dissolved.
    modifier onlyIfActive() {
        require(active == true, "EL");
        _;
    }

    /// @notice Modifier that requires the msg.sender to be the owner of a given Shard
    /// @param shard The Shard, whose ownership is tested for.
    modifier onlyHolder(bytes32 shard) {
        require(infoByShard[shard].owner == msg.sender, "OH");
        _;
    }

    /// @notice Constructor function that pushes the first Shard being the property of the Shardable creator.
    constructor() {
        // passes full ownership to creator of contract
        _pushShard(1, 1, msg.sender, 0);
        active = true;
    }

    /// @notice Purchases a listed Shard for sale.
    /// @dev If the purchase is with tokens (ie. tokenAddress != 0x0), first call 'token.approve(Shardable.address, salePrice);'
    /// @param shard The shard of which a fraction will be purchased.
    function purchase(bytes32 shard, uint256 amount) external payable onlyValidShard(shard) {
        require(shardsForSale[shard], "NS");
        require(saleByShard[shard].amount != 0, "ES");
        require(saleByShard[shard].amount >= amount, "ES");
        require((saleByShard[shard].to == msg.sender) || (saleByShard[shard].to == address(0x0)), "SR");
        _cancelSale(shard);
        uint256 totalPrice = amount * saleByShard[shard].price;
        (uint256 profitToCounekt, uint256 profitToSeller, uint256 remainder) = divideUnequallyIntoTwoWithRemainder(totalPrice,25,1000);
        profitToSeller += remainder; // remainder goes to seller
        // if ether
        if (saleByShard[shard].tokenAddress == address(0x0)) {
            require(msg.value >= totalPrice, "IE");
            // Pay Service Fee of 2.5% to Counekt
            (bool successToCounekt,) = payable(0x49a71890aea5A751E30e740C504f2E9683f347bC).call{value:profitToCounekt}("");
            // Rest goes to the seller
            (bool successToSeller,) = payable(infoByShard[shard].owner).call{value:profitToSeller}("");
            require(successToSeller && successToCounekt, "TF");
        } 
        else {
            ERC20 token = ERC20(saleByShard[shard].tokenAddress);
            require(token.allowance(msg.sender,address(this)) >= totalPrice,"IT");
            // Pay Service Fee of 2.5% to Counekt
            token.transferFrom(msg.sender, 0x49a71890aea5A751E30e740C504f2E9683f347bC, profitToCounekt);
            // Rest goes to the seller
            token.transferFrom(msg.sender,infoByShard[shard].owner,profitToSeller);
        }
        _split(shard, amount,msg.sender);
        if (infoByShard[shard].owner == this(address)) { // if newly issued shards
            // add those to the outstanding shard amount
            totalShardAmountByClock[clock] += amount;
        }
        emit SaleSold(shard,amount,msg.sender,saleByShard[shard].tokenAddress,saleByShard[shard].price);
        // if not whole shard is bought
        if (saleByShard[shard].amount != amount) { 
            // put the rest to sale again
            _putForSale(shardByOwner[infoByShard[shard].owner],saleByShard[shard].amount-amount,tokenAddress,price,to);
        }
    }

    /// @notice Puts a given shard for sale.
    /// @param shard The shard to be put for sale.
    /// @param amount Amount of the Shard to be put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to The specifically set buyer of the sale. Open to anyone, if address(0).
    function putForSale(bytes32 shard, uint256 amount, address tokenAddress, uint256 price, address to) public onlyHolder(shard) onlyValidShard(shard) {
        _putForSale(shard,amount,tokenAddress,price,to);
    }

    /// @notice Cancels a sell of a given shard.
    /// @param shard The shard to be put off sale.
    function cancelSale(bytes32 shard) public onlyHolder(shard) onlyValidShard(shard) {
        require(shardsForSale[shard], "NS");
        _cancelSale(shard);
    }

    /// @notice Splits a currently valid shard into two new ones. One is assigned to the receiver. The rest to the previous owner.
    /// @param senderShard The shard to be split.
    /// @param amount Amount, which will be subtracted from the previous shard and sent to the receiver.
    /// @param to The receiver of the new Shard.
    function split(bytes32 senderShard, uint256 amount, address to) public onlyHolder(senderShard) onlyValidShard(senderShard) {
        _split(senderShard,amount,to);
    }

    /// @notice Returns the clock.
    function getCurrentClock() public view returns(uint256) {
        return clock;
    }

    /// @notice Returns the clock, in which a shard will or has expired.
    function getShardExpirationClock(bytes32 shard) public view returns(uint256) {
        return shardExpirationClock[shard];
    }

    /// @notice Returns the price, at which a shard is for sale.
    function getShardSalePrice(bytes32 shard) public view returns(uint256) {
        return saleByShard[shard].price;
    }

    /// @notice Returns a boolean stating if a given shard is currently valid or not.
    /// @param shard The shard, whose validity is to be checked for.
    function isValidShard(bytes32 shard) public view returns(bool) {
        return getShardExpirationClock(shard) > clock;
    }

    /// @notice Checks if address is a shard holder - at least a partial owner of the contract.
    /// @param account The address to be checked for.
    function isShardHolder(address account) public view returns(bool) {
        return isValidShard(shardByOwner[account]);
    }
    
    /// @notice Returns a boolean stating if the given shard was valid at a given clock.
    /// @param shard The shard, whose validity is to be checked for.
    /// @param atClock The clock to be checked for.
    function shardExisted(bytes32 shard, uint256 atClock) public view returns(bool) {
        return infoByShard[shard].creationClock <= atClock && atClock < getShardExpirationClock(shard);
    }

    function _issueShards(uint256 amount, address tokenAddress, uint256 price, address to) {
        _expireShard(shardByOwner[this(address)],clock);
        _pushShard(amount+infoByShard[shardByOwner[this(address)]].amount,this(address),clock);
        _putForSale(shardByOwner[this(address)],amount,tokenAddress,price,to);
    }

    /// @notice Cancels a sell of a given Shard.
    /// @param shard The shard to be put off sale.
    function _cancelSale(bytes32 shard) internal onlyValidShard(shard) {
        shardsForSale[shard] = false;
    }

    /// @notice Splits a currently valid shard into two new ones. One is assigned to the receiver. The rest to the previous owner.
    /// @param senderShard The shard to be split.
    /// @param amount Amount, which will be subtracted from the previous shard and sent to the receiver.
    /// @param to The receiver of the new Shard.
    function _split(bytes32 senderShard, uint256 amount, address to) internal onlyValidShard(senderShard) onlyIfActive incrementClock {
        require(amount < infoByShard[senderShard].amount, "IA");
        if (isShardHolder(to)) { // if Receiver already owns a shard
            // The amounts are added and the shard thereby upgraded
            uint256 sumAmount = amount + infoByShard[shardByOwner[to]].amount;
            _pushShard(sumAmount,to,clock);
            // Expire the Old Receiver Shard
            _expireShard(shardByOwner[to], clock);
        }

        else {
            // The amount of the Receiver Shard is equal to the one split off of the Sender Shard
            _pushShard(amount,to,clock);
        }

        // Expire the Old Sender Shard
        _expireShard(senderShard, clock);
        // The new amount of the Sender Shard has been subtracted by the Split amount.
        diff = infoByShard[senderShard].amount - amount;
        if (diff != 0) {
        _pushShard(diff,infoByShard[senderShard].owner,clock);
        }
        emit SaleSold(senderShard,amount,to,address(0),0);
    }

    /// @notice Puts a given shard for sale.
    /// @param shard The shard to be put for sale.
    /// @param amount Amount of the Shard to be put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to The specifically set buyer of the sale. For anyone to buy if address(0).
    function _putForSale(bytes32 shard, uint256 amount, address tokenAddress, uint256 price, address to) internal onlyValidShard(shard) onlyIfActive {
        require(shardsForSale[shard] == false);
        require(amount <= infoByShard[shard].amount, "IA");
        saleByShard[shard] = ShardSale({
            amount: amount,
            tokenAddress: tokenAddress,
            price: price,
            to: to
        });
        shardsForSale[shard] = true;
        emit PutForSale(shard,amount,tokenAddress,price,to);
    }

    /// @notice Pushes a shard to the registry of currently valid shards.
    /// @param amount Amount of the Shard represents.
    /// @param owner The owner of the Shard.
    /// @param creationClock The clock at which the Shard will be created.
    function _pushShard(uint256 amount, address owner, uint256 creationClock) internal {
        // The representation, bytes and hash
        bytes32 shard = keccak256(abi.encodePacked(owner,creationClock));
        shardByOwner[owner] = shard;
        shardExpirationClock[shard] = type(uint256).max; // The maximum value: (2^256)-1;
        // The info, attributes and details
        infoByShard[shard] = ShardInfo({
                                amount:amount,
                                owner: owner,
                                creationClock: creationClock
                                });
        emit NewShard(shard,owner,creationClock);

    }

    /// @notice Removes a shard from the registry of currently valid shards.
    /// @param shard The shard to be expired.
    /// @param expirationClock The clock at which the Shard will expire.
    function _expireShard(bytes32 shard, uint256 expirationClock) internal {
        shardByOwner[infoByShard[shard].owner] = bytes32(0);
        shardExpirationClock[shard] = expirationClock;
        emit ExpiredShard(shard,expirationClock);
    }

}