USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_UserAgreement]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_UserAgreement](
	[AgreementID] [int] IDENTITY(1,1) NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[VGProductID] [int] NOT NULL,
	[UserName] [varchar](50) NOT NULL,
	[PersonName] [varchar](50) NULL,
	[Title] [varchar](50) NULL,
	[LegalName] [varchar](50) NULL,
	[BiddingType] [varchar](50) NULL,
	[BiddingAddress] [varchar](50) NULL,
	[BiddingState] [varchar](50) NULL,
	[PhysicalAddress] [varchar](50) NULL,
	[MailingAddress] [varchar](50) NULL,
	[BiddingEntity] [varchar](50) NULL,
	[AgreementDate] [datetime] NULL,
 CONSTRAINT [PK_vg_UserAgreement] PRIMARY KEY CLUSTERED 
(
	[AgreementID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
