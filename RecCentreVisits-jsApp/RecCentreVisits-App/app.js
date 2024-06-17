'use strict';

import { Rettiwt } from 'rettiwt-api';
import * as fs from 'fs';
//import { CursoredData } from '../node_modules/rettiwt-api/dist/index';

// Creating a new Rettiwt instance using the given 'API_KEY'
const rettiwt = new Rettiwt({ apiKey: "" });

// Fetching the details of the tweet with the id '1234567890'
/* rettiwt.tweet.details('1800128857296839126')
    .then(res => {
        console.log(res.fullText);
    })
    .catch(err => {
        console.log(err);
    });*/

let txt = "";

//let savedData = CursoredData;
let savedCurser = "";

rettiwt.user.timeline('297549322')
    .then(res => {
        for (let i = 0; i < 20; i++) {
            //savedData = res;
            savedCurser = res.next;
            let tweet = res.list[i].fullText;
            let dateAndTime = res.list[i].createdAt;
            let next = res.next.value;
            let indexStart = tweet.indexOf("WR") + 3;
            let indexEnd = tweet.indexOf("\n", indexStart);
            let num = tweet.substring(indexStart, indexEnd);
            for (let j = 0; j < num.length; j++) {
                if (isNaN(num[j])) {
                    num = num.substring(0, j);
                }
            }
            txt = dateAndTime + ", " + num + "\n" + txt;
        }

        rettiwt.user.timeline('297549322', 10)
            .then(res2 => {
                let tweet = res2.list[0].fullText;
                let dateAndTime = res2.list[0].createdAt;

                /*for (let i = 0; i < 20; i++) {
                    //savedCurser = res.next;
                    let tweet = res.list[i].fullText;
                    let dateAndTime = res.list[i].createdAt;
                    let next = res.next;
                    let indexStart = tweet.indexOf("WR") + 3;
                    let indexEnd = tweet.indexOf("\n", indexStart);
                    let num = tweet.substring(indexStart, indexEnd);
                    for (let j = 0; j < num.length; j++) {
                        if (isNaN(num[j])) {
                            num = num.substring(0, j);
                        }
                    }
                    txt = dateAndTime + ", " + num + "\n" + txt;
                }*/
            })
            .catch(err => {
                console.log(err);
            });

        // Write data in 'Output.txt' .
        fs.writeFile('Output.csv', txt, (err) => {

            // In case of a error throw err.
            if (err) throw err;
        })
    })
    .catch(err => {
        console.log(err);
    });




