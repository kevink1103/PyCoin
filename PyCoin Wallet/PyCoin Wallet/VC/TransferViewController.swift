//
//  TransferViewController.swift
//  PyCoin Wallet
//
//  Created by Kevin Kim on 10/12/2019.
//  Copyright © 2019 Kevin Kim. All rights reserved.
//

import UIKit

class TransferViewController: UIViewController, UITextViewDelegate, UITextFieldDelegate {
    
    let wallet = Wallet()
    let network = Network()
    
    @IBOutlet var addressView: UITextView!
    @IBOutlet var valueField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(DismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    @objc func DismissKeyboard(){
        //Causes the view to resign from the status of first responder.
        view.endEditing(true)
    }
    
    @IBAction func transferPressed(_ sender: Any) {
        if network.best.count <= 0 {
            let alert = UIAlertController(title: "Loading Best Node", message: "Please wait until the longest chain node is found.", preferredStyle: .alert)
            let ok = UIAlertAction(title: "OK", style: .default, handler: nil)
            alert.addAction(ok)
            self.present(alert, animated: true, completion: nil)
            return
        }
        
        if let recipient = addressView.text, recipient.count > 0, let value = valueField.text, value.count > 0 {
            let transaction = Transaction(wallet: wallet, recipient: recipient, value: value)
            if transaction.sign() {
                Network.newTransactionSigned(node: network.best, transaction: transaction, completionHandler: { status, result in
                    if status {
                        let alert = UIAlertController(title: "Transaction Submitted", message: "Transaction sent to \(self.network.best).", preferredStyle: .alert)
                        let ok = UIAlertAction(title: "OK", style: .default, handler: { _ in
                            self.dismiss(animated: true, completion: nil)
                        })
                        alert.addAction(ok)
                        self.present(alert, animated: true, completion: nil)
                    }
                })
            }
        }
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
    
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
        if segue.identifier == "ScannerSegue" {
            let destVC = segue.destination as! ScannerViewController
            destVC.parentVC = self
        }
    }

}
