def createMockDB():
    db  = {'games':{}, 'users':{}, 'emails_to_uids':{}, 'username_words_to_uids':{}, 'username_word_starts_to_uids':{}, 'events':[] }

    db['users']['ai'] = { 'usermail':"ai@watson.com",
                              'hashed_pass' : 'ai',
                              'username': "Computer",
                              'friends': [],
                              'incoming_friend_requests':[],
                              'outgoing_friend_requests':[],
                              'profile_image' : 'watson.jpg'
                            }
    db['emails_to_uids']['ai@watson.com'] = 'ai'
    
    db['users']['2'] = { 'usermail':"user2@test.com",
                              'hashed_pass' : 'ai',
                              'username': "TestUser2",
                              'friends': ["3", "ai"],
                              'incoming_friend_requests':[],
                              'outgoing_friend_requests':[],
                              'profile_image' : '2.jpg'
                            }
    db['emails_to_uids']['user1@test.com'] = '2'

    db['users']['3'] = { 'usermail':"user3@test.com",
                              'hashed_pass' : 'ai',
                              'username': "TestUser3",
                              'friends': ["1"],
                              'incoming_friend_requests':["4"],
                              'outgoing_friend_requests':[],
                              'profile_image' : '3.jpg'
                            }
    db['emails_to_uids']['user3@test.com'] = '3'

    db['users']['4'] = { 'usermail':"user4@test.com",
                              'hashed_pass' : 'ai',
                              'username': "TestUser4",
                              'friends': [],
                              'incoming_friend_requests':[],
                              'outgoing_friend_requests':["3"],
                              'profile_image' : '4.jpg'
                            }
    db['emails_to_uids']['user4@test.com'] = '4'

    db['users']['g7'] = { "username" : "Guest_7",
                              "hashed_pass" : None,
                              "usermail" : None,
                              "friends" : None,
                              "incoming_friend_requests" : None,
                              "outgoing_friend_requests" : None,
                              "profile_image" : None
                            }

    db['games']['1']={
                                "answer":"TESTINGWORD",
                                "incorrect_letters" : ['A', 'C'],
                                "incorrect_words" : ['TESTBADWORD'],
                                "correct_letters" : ['E', 'R', 'D', 'T'],
                                "is_ai":False,
                                "guesser_uid":"3",
                                "creator_uid":"g7",
                                "win":None
                            }

    db['games']['2']={
                                "answer":"TEST",
                                "incorrect_letters" : ['A', 'M', 'L', 'R'],
                                "is_ai":False,
                                "incorrect_words" : [],
                                "correct_letters" : ['E', 'S'],
                                "guesser_uid":"2",
                                "creator_uid":"4",
                                "win":None
                            }

    return db
