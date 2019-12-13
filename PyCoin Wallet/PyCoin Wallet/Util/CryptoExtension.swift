//
//  CryptoExtension.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import Foundation
import CryptoKit

// CryptoKit.Digest utils
extension Digest {
    var bytes: [UInt8] { Array(makeIterator()) }
    var data: Data { Data(bytes) }

    var hexStr: String {
        bytes.map { String(format: "%02X", $0) }.joined()
    }
}

extension SHA256 {
    static func hash(string: String) -> String? {
        guard let data = string.data(using: .utf8) else { return nil }
        let digest = SHA256.hash(data: data)
        return digest.hexStr.lowercased()
    }
}

extension Data {
    // init?(hexString: String) {
    //     let length = hexString.count / 2
    //     var data = Data(capacity: length)
    //     for i in 0 ..< length {
    //         let j = hexString.index(hexString.startIndex, offsetBy: i * 2)
    //         let k = hexString.index(j, offsetBy: 2)
    //         let bytes = hexString[j..<k]
    //         if var byte = UInt8(bytes, radix: 16) {
    //             data.append(&byte, count: 1)
    //         } else {
    //             return nil
    //         }
    //     }
    //     self = data
    // }
    
    struct HexEncodingOptions: OptionSet {
        let rawValue: Int
        static let upperCase = HexEncodingOptions(rawValue: 1 << 0)
    }

    func hexEncodedString(options: HexEncodingOptions = []) -> String {
        let format = options.contains(.upperCase) ? "%02hhX" : "%02hhx"
        return map { String(format: format, $0) }.joined()
    }
}
