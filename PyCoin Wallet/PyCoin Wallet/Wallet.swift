//
//  Wallet.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import Foundation
import SwiftyRSA

class Wallet {
    var publicKey: PublicKey? = nil
    var privateKey: PrivateKey? = nil
    
    init() {
        loadKey()
    }
    
    func loadKey() {
        if let publicKey = UserDefaults.standard.string(forKey: "public"), let privateKey = UserDefaults.standard.string(forKey: "private") {
            // print("LOAD EXISTING")
            self.publicKey = try? PublicKey(pemEncoded: publicKey)
            self.privateKey = try? PrivateKey(pemEncoded: privateKey)
        }
        else {
            // print("GENERATE NEW")
            let keyPair = generateKey()
            guard let publicKey = keyPair?.publicKey else { return }
            guard let privateKey = keyPair?.privateKey else { return }
            self.publicKey = publicKey
            self.privateKey = privateKey
            UserDefaults.standard.setValue(try? publicKey.pemString(), forKeyPath: "public")
            UserDefaults.standard.setValue(try? privateKey.pemString(), forKeyPath: "private")
        }
    }
    
    func generateKey() -> (privateKey: PrivateKey, publicKey: PublicKey)? {
        let keyPair = try? SwiftyRSA.generateRSAKeyPair(sizeInBits: 1024)
        return keyPair
    }
    
    var exportPublicKey: String {
        guard let data = try? self.publicKey?.data() else { return "" }
        return data.hexEncodedString()
    }
    
    var exportPrivateKey: String {
        guard let data = try? self.privateKey?.data() else { return "" }
        return data.hexEncodedString()
    }
}
