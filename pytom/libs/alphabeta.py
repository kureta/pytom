from itertools import cycle

from pytom.libs.euclid import euclid

alphabet_names = {'α': 'αλφα',
                  'β': 'βητα',
                  'γ': 'γαμμα',
                  'δ': 'δελτα',
                  'ε': 'εψιλον',
                  'ζ': 'ζητα',
                  'η': 'ητα',
                  'θ': 'θητα',
                  'ι': 'ιωτα',
                  'κ': 'καππα',
                  'λ': 'λαμδα',
                  'μ': 'μυ',
                  'ν': 'νυ',
                  'ξ': 'ξι',
                  'ο': 'ομικρον',
                  'π': 'πι',
                  'ρ': 'ρω',
                  'σ': 'σιγμα',
                  'τ': 'ταυ',
                  'υ': 'υψιλον',
                  'φ': 'φι',
                  'χ': 'χι',
                  'ψ': 'ψι',
                  'ω': 'ωμεγα'}

alphabet = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ',
            'χ', 'ψ', 'ω']

notes = ['do', 'dosd', 'dod', 'dodsd', 're', 'resd', 'red', 'redsd', 'mi', 'misd', 'fa', 'fasd', 'fad', 'fadsd', 'sol',
         'solsd', 'sold', 'soldsd', 'la', 'lasd', 'lad', 'ladsd', 'si', 'sisd']


def main():
    seed = 'α'
    tree = []

    # 6
    for _ in range(4):
        tree = [alphabet_names[letter] for letter in seed]
        seed = ''.join(tree)

    n2 = cycle(euclid(8, 3))
    durations = ('8.' if n == 3 else '8' for n in n2)

    chords = [[alphabet.index(letter) for letter in word] for word in tree]
    chords = [[notes[p] + '\'' for p in chord] for chord in chords]

    result = ['<{}>'.format(' '.join(chord)) + duration for chord, duration in zip(chords, durations)]

    text = ' '.join(result)
    print(text)


if __name__ == '__main__':
    main()
