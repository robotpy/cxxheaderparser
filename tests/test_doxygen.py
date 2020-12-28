# Note: testcases generated via `python -m cxxheaderparser.gentest`

from cxxheaderparser.types import (
    AnonymousName,
    Array,
    BaseClass,
    ClassDecl,
    EnumDecl,
    Enumerator,
    Field,
    ForwardDecl,
    Function,
    FundamentalSpecifier,
    Method,
    MoveReference,
    NameSpecifier,
    Operator,
    PQName,
    Parameter,
    Pointer,
    Reference,
    TemplateArgument,
    TemplateDecl,
    TemplateSpecialization,
    TemplateTypeParam,
    Token,
    Type,
    Typedef,
    UsingDecl,
    Value,
    Variable,
)
from cxxheaderparser.simple import (
    ClassScope,
    NamespaceScope,
    parse_string,
    ParsedData,
)

r"""
class SampleClass: public BaseSampleClass
{
public:
	enum Elephant
	{
		EL_ONE = 1,
		EL_TWO = 2,
		EL_NINE = 9,
		EL_TEN,
	};

    SampleClass();
    /*!
     * Method 1
     */
    string meth1();

    ///
    /// Method 2 description
    ///
    /// @param v1 Variable 1
    ///
    int meth2(int v1);

    /**
     * Method 3 description
     *
     * \param v1 Variable 1 with a really long
     * wrapping description
     * \param v2 Variable 2
     */
    void meth3(const string & v1, vector<string> & v2);

    /**********************************
     * Method 4 description
     *
     * @return Return value
     *********************************/
    unsigned int meth4();
private:
    void * meth5(){return NULL;}

    /// prop1 description
    string prop1;
    //! prop5 description
    int prop5;

    bool prop6;     /*!< prop6 description */

    double prop7;   //!< prop7 description
                    //!< with two lines
    
    /// prop8 description
    int prop8;
};
namespace Alpha
{
    class AlphaClass
    {
    public:
    	AlphaClass();

    	void alphaMethod();

    	string alphaString;
    protected:
    	typedef enum
    	{
    		Z_A,
    		Z_B = 0x2B,
    		Z_C = 'j',
			Z_D,
    	} Zebra;
    };

    namespace Omega
    {
		class OmegaClass
		{
		public:
			OmegaClass();

			string omegaString;
		protected:
			///
			/// @brief Rino Numbers, not that that means anything
			///
			typedef enum
			{
				RI_ZERO, /// item zero
				RI_ONE,  /** item one */
				RI_TWO,   //!< item two
				RI_THREE,
				/// item four
				RI_FOUR,
			} Rino;
		};
    };
}

"""


# def test_doxygen_messy():
#     content = """
#       // clang-format off

#       /// fn comment
#       void
#       fn();

#       /// var comment
#       int
#       v1 = 0;

#       int
#       v2 = 0; /// var2 comment

#       /// cls comment
#       class
#       C {};

#       /// template comment
#       template <typename T>
#       class
#       C2 {};
#     """
#     data = parse_string(content, cleandoc=True)

#     assert data == ParsedData(
#         namespace=NamespaceScope(
#             classes=[
#                 ClassScope(
#                     class_decl=ClassDecl(
#                         typename=PQName(
#                             segments=[NameSpecifier(name="C")], classkey="class"
#                         ),
#                         doxygen="/// cls comment",
#                     )
#                 ),
#                 ClassScope(
#                     class_decl=ClassDecl(
#                         typename=PQName(
#                             segments=[NameSpecifier(name="C2")], classkey="class"
#                         ),
#                         template=TemplateDecl(
#                             params=[TemplateTypeParam(typekey="typename", name="T")]
#                         ),
#                         doxygen="/// template comment",
#                     )
#                 ),
#             ],
#             functions=[
#                 Function(
#                     return_type=Type(
#                         typename=PQName(segments=[FundamentalSpecifier(name="void")])
#                     ),
#                     name=PQName(segments=[NameSpecifier(name="fn")]),
#                     parameters=[],
#                     doxygen="/// fn comment",
#                 )
#             ],
#             variables=[
#                 Variable(
#                     name=PQName(segments=[NameSpecifier(name="v1")]),
#                     type=Type(
#                         typename=PQName(segments=[FundamentalSpecifier(name="int")])
#                     ),
#                     value=Value(tokens=[Token(value="0")]),
#                     doxygen="/// var comment",
#                 ),
#                 Variable(
#                     name=PQName(segments=[NameSpecifier(name="v2")]),
#                     type=Type(
#                         typename=PQName(segments=[FundamentalSpecifier(name="int")])
#                     ),
#                     value=Value(tokens=[Token(value="0")]),
#                 ),
#             ],
#         )
#     )
