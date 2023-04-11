pragma solidity ^0.8.4;

import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @notice Returns a boolean stating if two given fractions are identical.
/// @param numerator1 Numerator of first fraction.
/// @param denominator1 Denominator of first fraction.
/// @param numerator2 Numerator of second fraction.
/// @param denominator2 Denominator of second fraction.
function fractionsAreIdentical(uint256 numerator1, uint256  denominator1, uint256 numerator2, uint256 denominator2) returns(bool) {
    return numerator1 == numerator2 && denominator1 == denominator2;
}

/// @notice Returns the two quotients and the remainder of an uneven division with a fraction. Useful for dividing ether and tokens.
/// @param dividend The dividend, which will be divided by the fraction.
/// @param numerator Numerator of fraction, which the dividend will be divided into.
/// @param denominator Denominator of fraction, which the dividend will be divided into.
function divideUnequallyIntoTwoWithRemainder(uint256 dividend, uint256 numerator, uint256 denominator) returns(uint256, uint256, uint256) {
    require(denominator > numerator);
    uint256 quotient1 = dividend*numerator/denominator;
    uint256 quotient2 = dividend*(denominator-numerator)/denominator;
    return (quotient1, quotient2, dividend - (quotient1 + quotient2));
}

/// @notice Returns the common denominator between two integers.
/// @param a First integer.
/// @param b Second integer.
function getCommonDenominator(uint256 a, uint256 b) pure returns(uint256) {
        while (b > 0) {
        (a, b) = (b, a % b);
        }
        return a;
}

/// @notice Returns a simplified version of a fraction.
/// @param numerator Numerator of fraction to be simplified.
/// @param denominator Denominator of fraction to be simplified.
function simplifyFraction(uint256 numerator, uint256 denominator) pure returns(uint256, uint256) {
    uint256 commonDenominator = getCommonDenominator(numerator,denominator);
    return (numerator/commonDenominator,denominator/commonDenominator);
}

/// @notice Adds two fractions together.
/// @param numerator1 Numerator of first fraction.
/// @param denominator1 Denominator of first fraction.
/// @param numerator2 Numerator of second fraction.
/// @param denominator2 Denominator of second fraction.
function addFractions(uint256 numerator1, uint256  denominator1, uint256 numerator2, uint256 denominator2) pure returns (uint256, uint256) {
    numerator1 = numerator1 * denominator2;
    numerator2 = numerator2 * denominator1;
    return (numerator1+numerator2,denominator1*denominator2);
}

/// @notice Subtracts a fraction from another and returns the difference.
/// @param numerator1 Numerator of minuend fraction.
/// @param denominator1 Denominator of minuend fraction.
/// @param numerator2 Numerator of subtrahend fraction.
/// @param denominator2 Denominator of subtrahend fraction.
function subtractFractions(uint256 numerator1, uint256 numerator2, uint256  denominator1, uint256 denominator2) pure returns (uint256,uint256) {
    numerator1 = numerator1 * denominator2;
    numerator2 = numerator2 * denominator1;
    return (numerator1-numerator2,denominator1*denominator2);
}


/// @title A shardable/fractional non-fungible token that can be fractually owned via Shards.
/// @author Frederik W. L. Christoffersen
/// @notice This contract is used to fractionalize a non-fungible token. Be aware that a sell transfers a service fee of 2.5% to Counekt.
/// @dev historicShards are used to show proof of ownership at different points of time.
/// @custom:beaware This is a commercial contract.
contract Shardable {

    /// @notice A struct representing the related info of a non-fungible Shard token.
    /// @dev Is represented via a bytes32 value created from the hash: keccak256(owner, creationTime).
    /// @param numerator Numerator of the fraction that the Shard represents.
    /// @param denominator Denominator of the fraction that the Shard represents.
    /// @param owner The owner of the Shard.
    /// @param creationTime The clock at which the Shard was created.
    /// @param expiredTime The clock at which the Shard expired. Default is set to the maximum value.
    struct ShardInfo {
        uint256 numerator;
        uint256 denominator;
        address owner; 
        uint256 creationTime;        
    }

    /// @notice A struct representing the related sale info of a non-fungible Shard token.
    /// @param forSaleTo Address pointing to a potentially specifically set buyer of the sale.
    /// @param numerator Numerator of the fraction that is for sale.
    /// @param denominator Denominator of the fraction that is for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param salePrice The amount which the Shard is for sale as. The token address being the valuta.
    struct ShardSale {
        address forSaleTo;
        uint256 numerator;
        uint256 denominator;
        address tokenAddress;
        uint256 salePrice;
    }

    /// @notice Integer value to implement a concept of time
    uint256 clock = 0;

    /// @notice Boolean stating if the Shardable is active and tradeable or not.
    bool public active = true;
    /// @notice Mapping pointing to related info of a Shard given the bytes of a unique Shard instance.
    mapping(bytes32 => ShardInfo) public infoByShard;
    /// @notice Mapping pointing to a currently valid shard given the address of its owner.
    mapping(address => bytes32) public shardByOwner;
    /// @notice Mapping pointing to related sale info of a Shard given the bytes of a unique Shard instance.
    mapping(bytes32 => ShardSale) saleByShard;
    // @notice Mapping pointing to an expired time given a shard.
    mapping(bytes32 => uint256) shardExpiredTime;
    
    /// @notice Event emitted when a Shard is split into two and fractionally transferred.
    /// @param shard The Shard, which was split.
    /// @param numerator Numerator of the absolute fraction of the offspring Shard.
    /// @param denominator Denominator of the absolute fraction of the offspring Shard.
    /// @param to The receiver of the splitted Shard.
    event SplitMade(
        bytes32 shard,
        uint256 numerator,
        uint256 denominator,
        address to
        );

    /// @notice Event emitted when a sale of a Shard is sold.
    /// @param shard The shard that was sold from.
    /// @param numerator Numerator of the absolute fraction of the Shard that was sold.
    /// @param denominator Denominator of the absolute fraction of the Shard that was sold.
    /// @param tokenAddress The address of the token that was accepted in the purchase. A value of 0x0 represents ether.
    /// @param price The amount which the Shard was for sale for. The token address being the valuta.
    /// @param to The buyer of the sale.
    event SaleSold(
        bytes32 shard,
        uint256 numerator,
        uint256 denominator,
        address tokenAddress,
        uint256 price,
        address to
        );

    /// @notice Event emitted when a Shard is put up for sale.
    /// @param shard The shard that was put for sale.
    /// @param numerator Numerator of the absolute fraction of the Shard put for sale.
    /// @param denominator Denominator of the absolute fraction of the Shard put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to The specifically set buyer of the sale, if any.
    event PutForSale(
        bytes32 shard,
        uint256 numerator,
        uint256 denominator,
        address tokenAddress,
        uint256 price,
        address to
        );

    modifier incrementClock {
        _;
        clock++;
    }
    
    /// @notice Modifier that requires the msg.sender to be a current valid Shard holder.
    modifier onlyShardHolder {
        require(isShardHolder(msg.sender), "NVSH");
        _;
    }

    /// @notice Modifier that requires the msg.sender to have been a historic Shard holder.
    modifier onlyHistoricShardHolder {
        require(isHistoricShardHolder(msg.sender), "NHVSH");
        _;
    }

    /// @notice Modifier that requires a given Shard to be currently valid.
    modifier onlyValidShard(bytes32 shard) {
        require(isValidShard(shard), "NVS");
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
        require(infoByShard[shard].owner == msg.sender);
        _;
    }

    /// @notice Constructor function that pushes the first Shard being the property of the Shardable creator.
    constructor() {
        // passes full ownership to creator of contract
        _pushShard(1, 1, msg.sender, 0);
    }

    /// @notice Purchases a listed Shard for sale.
    /// @dev If the purchase is with tokens (ie. tokenAddress != 0x0), first call 'token.approve(Shardable.address, salePrice);'
    /// @param shard The shard of which a fraction will be purchased.
    function purchase(bytes32 shard) external payable onlyIfActive onlyValidShard(shard) {
        require(ShardSale[shard].forSale, "NFS");
        require((infoByShard[shard].forSaleTo == msg.sender) || (infoByShard[shard].forSaleTo == address(0x0)), "OFSTS");
        _cancelSale(shard);
        (uint256 profitToCounekt, uint256 profitToSeller, uint256 remainder) = divideUnequallyIntoTwoWithRemainder(infoByShard[shard].salePrice,25,1000);
        profitToSeller += remainder; // remainder goes to seller
        // if ether
        if (infoByShard[shard].tokenAddress == address(0x0)) {
            require(msg.value >= infoByShard[shard].salePrice, "NEEP");
            // Pay Service Fee of 2.5% to Counekt
            (bool successCounekt, ) = payable(0x49a71890aea5A751E30e740C504f2E9683f347bC).call{value:profitToCounekt}("");
            require(successCounekt, "TF");
            // Rest goes to the seller
            (bool successSeller, ) = payable(infoByShard[shard].owner).call{value:profitToSeller}("");
            require(successSeller, "TF");
        } 
        else {
            ERC20 token = ERC20(infoByShard[shard].tokenAddress);
            require(token.allowance(msg.sender,address(this)) >= infoByShard[shard].salePrice,"NETP");
            // Pay Service Fee of 2.5% to Counekt
            token.transferFrom(msg.sender, 0x49a71890aea5A751E30e740C504f2E9683f347bC, profitToCounekt);
            // Rest goes to the seller
            token.transferFrom(msg.sender,infoByShard[shard].owner,profitToSeller);
        } 
        if (fractionsAreIdentical(infoByShard[shard].numerator,infoByShard[shard].denominator,infoByShard[shard].numeratorForSale,infoByShard[shard].denominatorForSale)) {_transferShard(shard,msg.sender);}
        else {_split(shard, infoByShard[shard].numeratorForSale,infoByShard[shard].denominatorForSale,msg.sender);}
        emit SaleSold(shard,infoByShard[shard].numeratorForSale,infoByShard[shard].denominatorForSale,infoByShard[shard].tokenAddress,infoByShard[shard].salePrice,msg.sender);
    }

    /// @notice Puts a given shard for sale.
    /// @param shard The shard to be put for sale.
    /// @param numerator Numerator of the absolute fraction of the Shard to be put for sale.
    /// @param denominator Denominator of the absolute fraction of the Shard to be put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    function putForSale(bytes32 shard, uint256 numerator, uint256 denominator, address tokenAddress, uint256 price) public onlyHolder(shard) onlyValidShard(shard) {
        _putForSale(shard,numerator,denominator,tokenAddress,price);
    }

    /// @notice Puts a given shard for sale only to a specifically set buyer.
    /// @param shard The shard to be put for sale.
    /// @param numerator Numerator of the the absolute fraction of the shard to be put for sale.
    /// @param denominator Denominator of the the absolute fraction of the shard to be put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    /// @param to The specifically set buyer of the sale.
    function putForSaleTo(bytes32 shard, uint256 numerator, uint256 denominator, address tokenAddress, uint256 price, address to) public onlyHolder(shard) {
        saleByShard[shard].forSaleTo = to;
        _putForSale(shard,numerator,denominator,tokenAddress,price);
    }

    /// @notice Cancels a sell of a given Shard.
    /// @param shard The shard to be put off sale.
    function cancelSale(bytes32 shard) public onlyHolder(shard) onlyValidShard(shard) {
        _cancelSale(shard);
    }

    /// @notice Splits a currently valid shard into two new ones. One is assigned to the receiver. The rest to the previous owner.
    /// @param senderShard The shard to be split.
    /// @param numerator Numerator of the absolute fraction, which will be subtracted from the previous shard and sent to the receiver.
    /// @param denominator Denominator of the absolute fraction, which will be subtracted from the previous shard and sent to the receiver.
    /// @param to The receiver of the new Shard.
    function split(bytes32 senderShard, uint256 numerator, uint256 denominator, address to) public onlyHolder(senderShard) onlyValidShard(senderShard) {
        _split(senderShard,numerator,denominator,to);
    }

    /// @notice Sends a whole shard to a receiver.
    /// @param senderShard The shard to be transferred.
    /// @param to The receiver of the new Shard.
    function transferShard(bytes32 senderShard, address to) public onlyHolder(senderShard) onlyValidShard(senderShard) {
        _transferShard(senderShard,to);
    }

    function getShardExpiredTime(bytes32 shard) returns(uint256) {
        if (shardExpiredTime[shard] == 0) {
            return type(uint256).max; // The maximum value: (2^256)-1;
        }
        return shardExpiredTime[shard];

    }

    /// @notice Returns a boolean stating if a given shard is currently valid or not.
    /// @param shard The shard, whose validity is to be checked for.
    function isValidShard(bytes32 shard) public view returns(bool) {
        return getShardExpiredTime(shard) > clock;
    }

    /// @notice Checks if address is a shard holder - at least a partial owner of the contract.
    /// @param account The address to be checked for.
    function isShardHolder(address account) public view returns(bool) {
        return isValidShard(shardByOwner[account]);
    }

    /// @notice Returns a boolean stating if a given shard has ever been valid or not.
    /// @param shard The shard, whose validity is to be checked for.
    function isHistoricShard(bytes32 shard) public view returns(bool) {
        return shardExpiredTime[shard] != 0;
    }

    /// @notice Checks if address is a historic Shard holder - at least a previous partial owner of the contract
    /// @param account The address to be checked for.
    function isHistoricShardHolder(address account) public view returns(bool) {
        return isHistoricShard(shardByOwner[account]);
    }

    /// @notice Returns a boolean stating if the given shard was valid at a given timestamp.
    /// @param shard The shard, whose validity is to be checked for.
    /// @param time The timestamp to be checked for.
    function shardExisted(bytes32 shard, uint256 time) public view returns(bool) {
        return infoByShard[shard].creationTime <= time && time < getShardExpiredTime(shard);
    }

    /// @notice Cancels a sell of a given Shard.
    /// @param shard The shard to be put off sale.
    function _cancelSale(bytes32 shard) internal onlyValidShard(shard) {
        require(saleByShard[shard].numerator != 0, "SNFS");
        saleByShard[shard] = ShardSale();
    }

    /// @notice Splits a currently valid shard into two new ones. One is assigned to the receiver. The rest to the previous owner.
    /// @param senderShard The shard to be split.
    /// @param numerator Numerator of the absolute fraction, which will be subtracted from the previous shard and sent to the receiver.
    /// @param denominator Denominator of the absolute fraction, which will be subtracted from the previous shard and sent to the receiver.
    /// @param to The receiver of the new Shard.
    function _split(bytes32 senderShard, uint256 numerator, uint256 denominator, address to) internal onlyValidShard(senderShard) {
        require(numerator/denominator < infoByShard[senderShard].numerator/infoByShard[senderShard].denominator, "MTW");
        uint256 transferTime = clock;
        if (isShardHolder(to)) { // if Receiver already owns a shard
            // The fractions are added and upgraded
            (uint256 sumNumerator, uint256 sumDenominator) = addFractions(infoByShard[shardByOwner[to]].numerator,infoByShard[shardByOwner[to]].denominator,numerator,denominator);
            _pushShard(sumNumerator,sumDenominator,to,transferTime);

            // Expire the Old Receiver Shard
            _expireShard(shardByOwner[to], transferTime);

        }

        else {
            // The Fraction of the Receiver Shard is equal to the one split off of the Sender Shard
            _pushShard(numerator,denominator,to,transferTime);
        }


        // Expire the Old Sender Shard
        _expireShard(senderShard, transferTime);
        // The new Fraction of the Sender Shard has been subtracted by the Split Fraction.
        (uint256 diffNumerator, uint256 diffDenominator) = subtractFractions(infoByShard[senderShard].numerator,infoByShard[senderShard].denominator,numerator,denominator);
        _pushShard(diffNumerator,diffDenominator,infoByShard[senderShard].owner,transferTime);
        if (msg.sender != address(this)) {
            emit SplitMade(senderShard,numerator,denominator,to);
        }
        
    }

    /// @notice Sends a whole shard to a receiver.
    /// @param senderShard The shard to be transferred.
    /// @param to The receiver of the new Shard.
    function _transferShard(bytes32 senderShard, address to) internal onlyValidShard(senderShard) {
        uint256 transferTime = clock;
        if (isShardHolder(to)) {

            // Destroying the Old receiver
            _expireShard(shardByOwner[to], transferTime);

            // The fractions are added and upgraded,to,transferTime
            (uint256 numerator, uint256 denominator) = addFractions(infoByShard[senderShard].numerator,infoByShard[senderShard].denominator,infoByShard[shardByOwner[to]].numerator,infoByShard[shardByOwner[to]].denominator);
            _pushShard(numerator,denominator,to,transferTime);
        }
        else {
            _pushShard(infoByShard[senderShard].numerator,infoByShard[senderShard].denominator,to,transferTime);
        }

        // Destroying the Old sender
        _expireShard(senderShard, transferTime);
        
        if (msg.sender != address(this)) {
            emit SplitMade(senderShard,infoByShard[senderShard].numerator,infoByShard[senderShard].numerator,to);
        }
    }

    /// @notice Puts a given shard for sale.
    /// @param shard The shard to be put for sale.
    /// @param numerator Numerator of the absolute fraction of the Shard to be put for sale.
    /// @param denominator Denominator of the absolute fraction of the Shard to be put for sale.
    /// @param tokenAddress The address of the token that is accepted when purchasing. A value of 0x0 represents ether.
    /// @param price The amount which the Shard is for sale as. The token address being the valuta.
    function _putForSale(bytes32 shard, uint256 numerator, uint256 denominator, address tokenAddress, uint256 price) internal onlyValidShard(shard) {
        require(numerator/denominator <= infoByShard[shard].numerator/infoByShard[shard].denominator, "MTW");
        (saleByShard[shard].numeratorForSale, infoByShard[shard].denominatorForSale) = simplifyFraction(numerator,denominator);
        saleByShard[shard].tokenAddress = tokenAddress;
        saleByShard[shard].salePrice = price;
        emit PutForSale(shard,infoByShard[shard].numeratorForSale,infoByShard[shard].denominatorForSale,tokenAddress,price,infoByShard[shard].forSaleTo);
    }

    /// @notice Pushes a shard to the registry of currently valid shards.
    /// @param numerator Numerator of the fraction that the Shard represents.
    /// @param denominator Denominator of the fraction that the Shard represents.
    /// @param owner The owner of the Shard.
    /// @param creationTime The clock at which the Shard will be created.
    function _pushShard(uint256 numerator, uint256 denominator, address owner, uint256 creationTime) internal {
        // The representation, bytes and hash
        bytes32 shard = keccak256(abi.encodePacked(owner,creationTime));
        shardByOwner[owner] = shard;
        validShards[shard] = true;
        // The info, attributes and details
        infoByShard[shard] = ShardInfo({
                                numerator:numerator,
                                denominator:denominator,
                                owner: owner,
                                creationTime: creationTime
                                });
    }

    /// @notice Removes a shard from the registry of currently valid shards.
    /// @param shard The shard to be expired.
    /// @param expiredTime The clock at which the Shard will expire.
    function _expireShard(bytes32 shard, uint256 expiredTime) internal  {
        infoByShard[shard].expiredTime = expiredTime;
    }

}