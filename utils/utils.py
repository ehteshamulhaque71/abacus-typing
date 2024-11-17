class TypingUtils:
    def getFormattedSuggestions(self, suggestionList, start, inc):
        formattedSuggestion = ''
        idx = start
        if suggestionList[0] != '':
            formattedSuggestion += suggestionList[0] + ': ' + str(idx)
        for suggestion in suggestionList[1:]:
            if suggestion != '':
                idx += inc
                formattedSuggestion += ', ' + suggestion + ': ' + str(idx)
        return formattedSuggestion

    def getFormattedSuggestions2(self, suggestionList, gestureList):
        formattedSuggestion = ''
        idx = 0
        if suggestionList[0] != '':
            formattedSuggestion += suggestionList[0] + ': ' + gestureList[idx]
        for suggestion in suggestionList[1:]:
            idx += 1
            if suggestion != '':
                formattedSuggestion += ', ' + suggestion + ': ' + gestureList[idx]
        return formattedSuggestion
