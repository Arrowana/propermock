[![Build Status](https://travis-ci.com/Arrowana/propermock.svg?branch=master)](https://travis-ci.com/Arrowana/propermock)

# Summary

A strict mocking package for python 3. In short, it is the opposite of unittest.mock

DISCLAIMER: ABSOLUTELY NOT STABLE OR COMPLETE YET, DO NOT USE FOR UNIT TESTING

# Motivation

Provide a way to mock for unit tests

Avoid defining mock contract in the test itself which decentralizes class contracts and defeat the purpose of unit testing

Prevent any black magic side effects by testing with something which doesn't reflect at all the real implementation or abstract base class

Write unit test to test the designed behavior rather than unit test the way your code is implemented

This package does not provide the wrong way of doing things and other less terrible alternative :). It only provides what seems right

## Further design details

### Why do I have to set a return value for every single method call which is called?

We don't want to be returning magic objects that have no validity in the function under test context. Let's test with the type that the function under test will have to deal with

Moreover, we can't trust the function under test, let's prevent it from using what we don't expect it to use

### Why mock.method.returns() instead of mock.method.return_value

We live in a risky python world where attribute can be assigned at any time. Fine, but not during unit tests

### Where is the unittest.mock.patch, Mock or MagicMock equivalent in this package?

Well, our intent is to unit test not concoct a vicious witchcraft. We will be fine with propermock.Mock

# Documentation

The source code itself

# Goals

Mock basic class

Ensure signatures are respected (impossible to call method with wrong number of args)

A mock method need to always be setup to return an object, which matches the function return annotation

Make auto completion and type check possible for linters on mock (e.g.: mock.foo...)

Feature to verify call, number of calls and arguments

# Bonus: Unit testing chinese proverbs

Unit test your implementation, don't write "unit tests" to make your manager happy

Your unit tests should mind their own business

Mocks aren't stubs

Listen to your test suite

...