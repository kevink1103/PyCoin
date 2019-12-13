//
//  ViewController.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import UIKit
import SwiftyRSA

class ViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    var timer = Timer()
    let wallet = Wallet()
    let network = Network()
    
    @IBOutlet var addressLabel: UILabel!
    @IBOutlet var balanceLabel: UILabel!
    @IBOutlet var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        scheduledTimerWithTimeInterval()
        addressLabel.text = wallet.exportPublicKey
        // print(wallet.exportPublicKey)
        // print(wallet.exportPrivateKey)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        
    }
    
    func scheduledTimerWithTimeInterval() {
        // Scheduling timer to Call the function "updateCounting" with the interval of 1 seconds
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.updateData), userInfo: nil, repeats: true)
    }
    
    @objc func updateData() {
        network.loadNodes()
        network.updateNodes()
        if network.best.count > 0 {
            Network.getBalance(node: network.best, address: wallet.exportPublicKey, completionHandler: { status, balance in
                if status {
                    self.balanceLabel.text = "Balance: \(balance!) PYC"
                }
            })
        }
        tableView.reloadData()
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return network.nodes.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell: UITableViewCell = tableView.dequeueReusableCell(withIdentifier: "Cell")!
        cell.textLabel?.text = Array(network.nodes)[indexPath.row]
        return cell
    }
    
    @IBAction func clipboardPressed(_ sender: Any) {
        if wallet.exportPublicKey.count > 0 {
            UIPasteboard.general.string = wallet.exportPublicKey
            let alert = UIAlertController(title: "Copy Successful", message: "Your address is copied to clipboard.", preferredStyle: .alert)
            let ok = UIAlertAction(title: "OK", style: .default, handler: nil)
            alert.addAction(ok)
            self.present(alert, animated: true, completion: nil)
        }
    }

}

