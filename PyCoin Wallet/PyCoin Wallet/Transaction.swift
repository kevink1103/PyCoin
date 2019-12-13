//
//  Transaction.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import Foundation
import SwiftyRSA

class Transaction {
    
    var wallet: Wallet
    var sender: String
    var recipient: String
    var value: String
    var signature: String? = nil
    
    init(wallet: Wallet, recipient: String, value: String) {
        self.wallet = wallet
        self.sender = wallet.exportPublicKey
        self.recipient = recipient
        self.value = value
    }
    
    var payload: String {
        return "{'sender': '\(self.sender)', 'recipient': '\(self.recipient)', 'value': '\(self.value)'}"
    }
    
    func sign() -> Bool {
        guard let clear = try? ClearMessage(string: self.payload, using: .utf8) else { return false }
        guard let signature = try? clear.signed(with: self.wallet.privateKey!, digestType: .sha1) else { return false }
        let hexString = signature.data.hexEncodedString()
        self.signature = hexString
        return true
    }
    
}
