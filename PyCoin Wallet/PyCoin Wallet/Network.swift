//
//  Network.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import Foundation
import Alamofire

class Network {
    
    var nodes: Set<String> = Set()
    var best: String = ""
    var chain: String = ""
    
    init() {
        loadNodes()
        updateNodes()
        choosebestNode()
    }
    
    func loadNodes() {
        if let existingNodes = UserDefaults.standard.array(forKey: "nodes") {
            self.nodes = Set(existingNodes.map { $0 as! String })
        }
        else {
            self.nodes = Set(["3.14.150.107"])
        }
    }
    
    func updateNodes() {
        for node in self.nodes {
            Network.getNodes(node: node, completionHandler: { status, result in
                if status {
                    let dict = result! as! Dictionary<String, Array<String>>
                    let newNodes = Set(dict["nodes"]!)
                    for node in newNodes {
                        self.nodes.insert(node)
                    }
                    UserDefaults.standard.set(Array(self.nodes), forKey: "nodes")
                }
            })
        }
    }
    
    func choosebestNode() {
        var maxLength = 0
        var maxNode = ""
        
        DispatchQueue.global(qos: .background).async {
            let group = DispatchGroup()
            
            for node in self.nodes {
                group.enter()
                Network.getLightNode(node: node, completionHandler: { status, result in
                    if status {
                        let dict = result! as! Dictionary<String, Any>
                        if let lengthString = dict["length"] {
                            let length = lengthString as! Int
                            if length > maxLength {
                                maxLength = length
                                maxNode = node
                            }
                        }
                    }
                    group.leave()
                })
            }
            group.notify(queue: DispatchQueue.main, execute: {
                self.best = maxNode
            })
        }
    }
    
    static func getNodes(node: String, completionHandler: @escaping (Bool, NSDictionary?) -> ()) {
        AF.request("http://" + node + "/get_nodes", method: .get)
            .responseJSON { response in
                switch (response.result) {
                case .success(let result):
                    let data = result as! NSDictionary
                    completionHandler(true, data)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    
    static func getLightNode(node: String, completionHandler: @escaping (Bool, NSDictionary?) -> ()) {
        AF.request("http://" + node + "/lightweight", method: .get)
            .responseJSON { response in
                switch (response.result) {
                case .success(let result):
                    let data = result as! NSDictionary
                    completionHandler(true, data)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    
    static func getBalance(node: String, address: String, completionHandler: @escaping (Bool, String?) -> ()) {
        let parameter = ["address": address]
        AF.request("http://" + node + "/check_balance", method: .post, parameters: parameter)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    
    static func newTransactionSigned(node: String, transaction: Transaction, completionHandler: @escaping (Bool, String?) -> ()) {
        let parameter = [
            "sender": transaction.sender,
            "recipient_address": transaction.recipient,
            "value": transaction.value,
            "signature": transaction.signature
        ]
        AF.request("http://" + node + "/new_transaction_signed", method: .post, parameters: parameter)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
                
        }
        
    }
}

